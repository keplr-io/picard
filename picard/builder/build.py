from __future__ import absolute_import

from networkx.algorithms.dag import topological_sort
from keras.models import Model
from keras.layers import Input, merge

from .graph_utils import get_graph, get_graph_edge
from .operator_utils import get_operator_image
from keras import backend as K
from copy import deepcopy

def get_hypermodel_fitted_to_data(model_spec, data_spec):
    hypermodel = deepcopy(model_spec)
    for leg_spec in data_spec['in']:
        hypermodel['legs']['in'][
            leg_spec['leg']
        ]['shape'] = data_spec['fields'][leg_spec['field']]['shape']

    for leg_spec in data_spec['out']:
        hypermodel['legs']['out'][
            leg_spec['leg']
        ]['shape'] = data_spec['fields'][leg_spec['field']]['shape']

    return hypermodel

def build_model(model_spec, data_spec):

    hypermodel = get_hypermodel_fitted_to_data(model_spec, data_spec)
    print hypermodel
    '''
        Yields a compiled keras model
    '''
    if K.backend() == 'tensorflow':
        import tensorflow as tf

        old_session = K.get_session()
        if old_session != None:
            old_session.close()

        K.set_session(tf.Session(config=tf.ConfigProto(
            gpu_options=tf.GPUOptions(allow_growth=True)
        )))

    operator_images = get_operator_images(hypermodel)

    model = Model(
        input=[
            operator_images[leg_key]
            for leg_key in hypermodel['legs']['in']
        ],
        output=[
            operator_images[leg_key]
            for leg_key in hypermodel['legs']['out']
        ]
    )

    model.compile(
        loss=[
            leg_spec['loss'] if 'loss' in leg_spec else 'categorical_crossentropy'
            for leg_key, leg_spec in hypermodel['legs']['out'].iteritems()
        ],
        loss_weights=[
            leg_spec['loss_weight'] if 'loss_weight' in leg_spec else 1
            for leg_key, leg_spec in hypermodel['legs']['out'].iteritems()
        ],
        metrics=['accuracy'],
        **hypermodel['compile']
    )

    return model

def get_operator_images(model_spec):

    '''
    Yields a dict
    {
        [node key]: [operator composition result at node]
    }
    '''

    graph = get_graph(model_spec)

    def to_layers_map(comps_map, node_key):

        in_edges = graph.in_edges(node_key)

        if len(in_edges) == 0:

            comps_map.update({
                node_key: Input(
                    name=node_key,
                    **model_spec['legs']['in'][node_key]
                )
            })


        elif len(in_edges) == 1:
            comps_map.update({
                node_key: get_operator_image(
                    comps_map[in_edges[0][0]],
                    get_graph_edge(graph, in_edges[0])[0]['operator'],
                    in_edges[0][1],
                    model_spec['operators']
                )
            })

        else:
            comps_map.update({
                node_key: merge(
                    [
                        get_operator_image(
                            comps_map[in_edge[0]],
                            get_graph_edge(graph, in_edge)[0]['operator'],
                            in_edge[1],
                            model_spec['operators'],
                        )
                        for in_edge in in_edges
                    ],
                    mode='concat'
                )
            })

        return comps_map

    return reduce(
        to_layers_map,
        topological_sort(graph),
        {}
    )
