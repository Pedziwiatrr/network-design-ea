import matplotlib

matplotlib.use('Agg')
import collections
import networkx as nx
import matplotlib.pyplot as plt
import math


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


def visualize_network(network_data, filename="network_topology.png"):
    G = nx.Graph()

    nodes = set()
    for edge_set in network_data['edges']:
        for node in edge_set:
            nodes.add(node)

    G.add_nodes_from(nodes)

    edge_map = {}
    for edge_set in network_data['edges']:
        edge_list = list(edge_set)
        G.add_edge(edge_list[0], edge_list[1])
        edge_map[frozenset(edge_list)] = tuple(edge_list)

    pos = nx.spring_layout(G)

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')

    str_labels = {edge_map[frozenset(e)]: f"{e[0]}-{e[1]}" for e in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=str_labels)

    plt.title("Network Topology")
    plt.axis('off')
    plt.savefig(filename)
    plt.close()


def visualize_solution(network_data, individual, modularity_m, is_aggregation, filename="solution.png"):
    G = nx.Graph()
    nodes = set()
    for edge_set in network_data['edges']:
        for node in edge_set:
            nodes.add(node)
    G.add_nodes_from(nodes)

    edge_mapping = {}
    for edge_set in network_data['edges']:
        edge_list = list(edge_set)
        G.add_edge(edge_list[0], edge_list[1])
        edge_mapping[edge_set] = tuple(edge_list)

    pos = nx.spring_layout(G)

    edge_loads = {edge: 0 for edge in network_data['edges']}
    chromosome = individual['chromosome']

    if is_aggregation:
        for i, demand in enumerate(network_data['demands']):
            chosen_path_index = chromosome[i]
            chosen_path = network_data['paths'][demand['id']][chosen_path_index]
            demand_value = demand['value']
            for edge in chosen_path:
                if edge in edge_loads:
                    edge_loads[edge] += demand_value
    else:
        for i, demand in enumerate(network_data['demands']):
            path_ratios = chromosome[i]
            demand_value = demand['value']
            available_paths = network_data['paths'][demand['id']]
            for path_index, ratio in enumerate(path_ratios):
                flow_on_path = demand_value * ratio
                path = available_paths[path_index]
                for edge in path:
                    if edge in edge_loads:
                        edge_loads[edge] += flow_on_path

    edge_costs = {}
    edge_labels_cost = {}
    edge_widths = []

    max_load = 1
    all_loads = edge_loads.values()
    if any(all_loads):
        max_load = max(all_loads)
        if max_load == 0: max_load = 1

    for edge_fs in network_data['edges']:
        load = edge_loads[edge_fs]
        cost = 0
        if load > 0:
            cost = math.ceil(load / modularity_m)

        edge_costs[edge_fs] = cost

        nx_edge = edge_mapping.get(edge_fs)
        if not nx_edge:
            nx_edge = tuple(edge_fs)
            if not G.has_edge(*nx_edge):
                nx_edge = (nx_edge[1], nx_edge[0])

        edge_labels_cost[nx_edge] = f"L: {load:.1f}\nC: {cost}"
        edge_widths.append(1 + (load / max_load) * 8)

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='gray', alpha=0.7)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_cost, font_size=8, font_color='black')

    mode_str = "Aggregation" if is_aggregation else "Deaggregation"
    plt.title(f"Solution: {mode_str} (m={modularity_m})\nTotal Cost (Fitness): {individual['fitness']:.2f}")
    plt.axis('off')
    plt.savefig(filename)
    plt.close()


if __name__ == '__main__':
    net_data = get_network_data()
    visualize_network(net_data, "network_topology_test.png")