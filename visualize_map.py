import matplotlib.pyplot as plt
import networkx as nx
import os
import argparse
import numpy as np
from src.loader import SNDlibLoader
from src.ea import EvoSolver
from src import config


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


def visualize_network(file_path, chromosome, modularity):
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

    plt.title(f"Network Traffic Load (m={modularity})", fontsize=14)
    plt.axis("off")
    plt.tight_layout()

    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(config.RESULTS_DIR, "map_visualization.png")
    plt.savefig(output_path, dpi=300)
    print(f"Map saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default=config.DATA_FILE)
    parser.add_argument("--modularity", type=float, default=config.DEFAULT_MODULARITY)
    parser.add_argument("--pop", type=int, default=config.DEFAULT_POP_SIZE)
    parser.add_argument("--gens", type=int, default=config.DEFAULT_GENERATIONS)
    parser.add_argument(
        "--mutation_rate", type=float, default=config.DEFAULT_MUTATION_RATE
    )
    parser.add_argument("--alpha", type=float, default=config.DEFAULT_ALPHA)
    parser.add_argument("--deagg", action="store_true")
    args = parser.parse_args()

    is_aggregation = not args.deagg
    mode_name = "Deaggregation" if args.deagg else "Aggregation"

    print(
        f"MODULARITY: {args.modularity}, POPULATION SIZE: {args.pop}, GENERATION COUNT: {args.gens}, MUTATION RATE: {args.mutation_rate}, MODE: {mode_name}"
    )

    loader = SNDlibLoader()
    network = loader.load(args.file)

    solver = EvoSolver(
        network,
        modularity=args.modularity,
        aggregation=is_aggregation,
        pop_size=args.pop,
        generations=args.gens,
        mutation_rate=args.mutation_rate,
        alpha=args.alpha,
    )

    best_chromosome, best_cost, _, _ = solver.run()

    print(f"Best Cost found: {best_cost}")
    visualize_network(args.file, best_chromosome, args.modularity)
