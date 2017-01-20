'''
    Utitilies for hyperparamter model structure graph processing
'''


from networkx import MultiDiGraph

def get_graph(model_spec, debug=True):

    '''
        Builds a networkx representation of the graph,
    '''


    graph = MultiDiGraph()

    graph.add_nodes_from(
        list(model_spec['graph']['nodes']) +
        model_spec['legs']['incoming'].keys() +
        model_spec['legs']['outgoing'].keys()
    )

    print('-------------')
    print(
        model_spec['graph']['edges']
    )
    print (
        [
            edge for edge in model_spec['graph']['edges']
        ]
    )
    print('===============')

    graph.add_edges_from(
        [
            (edge['source'], edge['target'], {
                'operator': edge['operator']
            }) for edge in model_spec['graph']['edges']
        ]
    )

    if debug:
        draw_graph(graph)

    return graph

def get_graph_edge(graph, edge_tuple):
    return graph[edge_tuple[0]][edge_tuple[1]]


def draw_graph(graph):
    from networkx.drawing.nx_agraph import graphviz_layout
    from networkx import draw_networkx
    from matplotlib import pyplot as plt

    draw_networkx(graph, graphviz_layout(graph))
    plt.show()
