import matplotlib.pyplot as plt
import networkx as nx
import os
import numpy as np
from src.loader import SNDlibLoader
from src.ea import EvoSolver


def calculate_link_loads(network, chromosome):
    link_loads = {link.id: 0.0 for link in network.links.values()}
    demand_ids = sorted(network.demands.keys(), key=lambda x: int(x.split("_")[1]))

    for i, demand_id in enumerate(demand_ids):
        demand = network.demands[demand_id]
        paths = demand.admissable_paths

        if len(chromosome.shape) > 1:
            path_idx = np.argmax(chromosome[i])
        else:
            path_idx = int(chromosome[i])

        if path_idx < len(paths):
            selected_path = paths[path_idx]
            for link_id in selected_path:
                link_loads[link_id] += demand.value

    return link_loads


def visualize_network(file_path, chromosome):
    network = SNDlibLoader.load(file_path)
    link_loads = calculate_link_loads(network, chromosome)

    G = nx.Graph()

    pos = {}
    for node in network.nodes.values():
        G.add_node(node.id)
        pos[node.id] = (node.x, node.y)

    edges = []
    weights = []
    edge_labels = {}

    for link in network.links.values():
        load = link_loads[link.id]
        if load > 0:
            G.add_edge(link.source, link.target)
            edges.append((link.source, link.target))
            weights.append(load)
            edge_labels[(link.source, link.target)] = str(int(load))

    plt.figure(figsize=(12, 10))

    nx.draw_networkx_nodes(
        G, pos, node_size=700, node_color="lightblue", edgecolors="black"
    )

    label_pos = {k: (v[0], v[1] + 0.15) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, font_size=14, font_weight="bold")

    if weights:
        max_load = max(weights)
        norm_weights = [(w / max_load) * 7 + 1 for w in weights]
    else:
        norm_weights = 1

    nx.draw_networkx_edges(
        G, pos, edgelist=edges, width=norm_weights, edge_color="blue", alpha=0.6
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=12,
        font_color="black",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8),
    )

    plt.title("Network traffic", fontsize=18)
    plt.axis("off")
    plt.tight_layout()

    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "map_visualization.png")
    plt.savefig(output_path, dpi=300)
    print(f"Map saved to {output_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "data", "polska.txt")

    print("Generating solution...")

    loader = SNDlibLoader()
    network = loader.load(data_file)

    solver = EvoSolver(
        network,
        modularity=10,
        aggregation=True,
        pop_size=200,
        generations=50,
        mutation_rate=0.4,
    )

    best_chromosome, best_cost, _, _ = solver.run()

    print(f"Best Cost found: {best_cost}")
    visualize_network(data_file, best_chromosome)
