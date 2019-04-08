import networkx as nx
import matplotlib.pyplot as plt

def generate_graph_from_connections(connections):
    G = nx.Graph()
    
    for node in connections:
        for adjacent_node in connections[node]['friends']:
            adj_node_label = adjacent_node['name']
            G.add_edge(node, adj_node_label)
    
    return G
    
def viz_graph(G, save_graph=False, file_name='demo.png'):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=400)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(),
                       width=2)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    plt.axis('off')
    if save_graph:
        plt.savefig(file_name)
    else:
        plt.show()