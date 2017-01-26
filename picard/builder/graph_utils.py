'''
    Utitilies for hyperparamter model structure graph processing
'''


from networkx import MultiDiGraph

def get_graph(model_spec, debug=False):

    '''
        Builds a networkx representation of the graph,
    '''


    graph = MultiDiGraph()

    graph.add_nodes_from(
        get_nodes(model_spec['edges']) +
        model_spec['legs']['in'].keys() +
        model_spec['legs']['out'].keys()
    )


    graph.add_edges_from(
        [
            (edge['source'], edge['target'], {
                'operator': edge['operator']
            }) for edge in model_spec['edges']
        ]
    )

    if debug:
        draw_graph(graph)

    return graph

def get_nodes(edges):
    nodes = {}
    for edge in edges:
        nodes[edge['source']] = True
        nodes[edge['target']] = True
    return nodes.keys()

def get_graph_edge(graph, edge_tuple):
    return graph[edge_tuple[0]][edge_tuple[1]]


def draw_graph(graph):
    from networkx.drawing.nx_agraph import graphviz_layout
    from networkx import draw_networkx
    from matplotlib import pyplot as plt

    draw_networkx(graph, graphviz_layout(graph))
    plt.show()
