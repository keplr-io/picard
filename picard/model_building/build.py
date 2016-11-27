from __future__ import absolute_import

from networkx.algorithms.dag import topological_sort
from keras.models import Model
from keras.layers import Input, merge

from .graph_utils import get_graph, get_graph_edge
from .operator_utils import get_operator_image
import tensorflow as tf
from keras import backend as K

def build_model(model_spec):

    '''
        Yields a compiled keras model
    '''

    oldSession = K.get_session()
    if (oldSession != None):
        oldSession.close()

    K.set_session(tf.Session(config=tf.ConfigProto(
        gpu_options=tf.GPUOptions(
            allow_growth = True,
        )
    )))

    operator_images = get_operator_images(model_spec)

    model = Model(
        input=[
            operator_images[leg_key]
            for leg_key in model_spec['legs']['incoming']
        ],
        output=[
            operator_images[leg_key]
            for leg_key in model_spec['legs']['outgoing']
        ]
    )

    model.compile(
        loss=[
            leg_spec['loss']
            for leg_key, leg_spec in model_spec['legs']['outgoing'].iteritems()
        ],
        loss_weight=[
            leg_spec['loss_weight']
            for leg_key, leg_spec in model_spec['legs']['outgoing'].iteritems()
        ],
        metrics=['accuracy'],
        **model_spec['compile']
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
                    **model_spec['legs']['incoming'][node_key]
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
