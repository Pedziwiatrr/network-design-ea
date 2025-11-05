import collections
import networkx as nx
import matplotlib.pyplot as plt


def get_network_data():
    edges = {
        frozenset({'A', 'B'}),
        frozenset({'A', 'C'}),
        frozenset({'B', 'D'}),
        frozenset({'C', 'D'}),
        frozenset({'B', 'C'})
    }

    demands = [
        {'id': 0, 'source': 'A', 'target': 'D', 'value': 25},
        {'id': 1, 'source': 'B', 'target': 'C', 'value': 18}
    ]

    paths = {
        0: [
            [frozenset({'A', 'B'}), frozenset({'B', 'D'})],
            [frozenset({'A', 'C'}), frozenset({'C', 'D'})]
        ],
        1: [
            [frozenset({'B', 'C'})],
            [frozenset({'B', 'A'}), frozenset({'A', 'C'})],
            [frozenset({'B', 'D'}), frozenset({'D', 'C'})]
        ]
    }

    return {'edges': edges, 'demands': demands, 'paths': paths}


def visualize_network(network_data):
    G = nx.Graph()

    nodes = set()
    for edge_set in network_data['edges']:
        for node in edge_set:
            nodes.add(node)

    G.add_nodes_from(nodes)

    for edge_set in network_data['edges']:
        edge_list = list(edge_set)
        G.add_edge(edge_list[0], edge_list[1])

    pos = nx.spring_layout(G)

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{u}-{v}' for u, v in G.edges()})

    demand_labels = {}
    for demand in network_data['demands']:
        demand_labels[f"D{demand['id']}"] = f"{demand['source']}->{demand['target']} ({demand['value']})"

    plt.title("Example Network Topology with Demands")
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    net_data = get_network_data()
    visualize_network(net_data)