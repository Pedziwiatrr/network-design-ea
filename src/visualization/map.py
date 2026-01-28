import sys
import os

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx
import argparse
import numpy as np
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from src.utils.loader import SNDlibLoader
from src.ea import EvoSolver
from src import config


def calculate_link_loads(network, chromosome, is_aggregation):
    link_loads = {link.id: 0.0 for link in network.links.values()}
    demand_ids = sorted(network.demands.keys(), key=lambda x: int(x.split("_")[1]))

    for i, demand_id in enumerate(demand_ids):
        demand = network.demands[demand_id]
        paths = demand.admissable_paths

        if len(chromosome.shape) > 1:
            weights = chromosome[i]

            if is_aggregation:
                # Aggregation: Winner takes all
                chosen_idx = np.argmax(weights)
                if chosen_idx < len(paths):
                    for link_id in paths[chosen_idx]:
                        link_loads[link_id] += demand.value
            else:
                # Deaggregation: Proportional split
                total_w = np.sum(weights)
                if total_w > 0:
                    weights = weights / total_w

                for p_idx, path in enumerate(paths):
                    flow = demand.value * weights[p_idx]
                    if flow > 0:
                        for link_id in path:
                            link_loads[link_id] += flow
        else:
            path_idx = int(chromosome[i])
            if path_idx < len(paths):
                selected_path = paths[path_idx]
                for link_id in selected_path:
                    link_loads[link_id] += demand.value

    total_flow = sum(link_loads.values())
    print(f"TOTAL FLOW: {total_flow}")
    return link_loads


def visualize_network(file_path, chromosome, modularity, is_aggregation):
    network = SNDlibLoader.load(file_path)
    link_loads = calculate_link_loads(network, chromosome, is_aggregation)

    G = nx.Graph()

    xs = []
    ys = []
    pos = {}
    for node in network.nodes.values():
        G.add_node(node.id)
        pos[node.id] = (node.x, node.y)
        xs.append(node.x)
        ys.append(node.y)

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

    plt.figure(figsize=(12, 12))

    img_path = os.path.join(os.path.dirname(file_path), "polska.png")

    if os.path.exists(img_path):
        try:
            img = mpimg.imread(img_path)
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            margin_x = (max_x - min_x) * 0.1
            margin_y = (max_y - min_y) * 0.1

            extent = [
                min_x - margin_x,
                max_x + margin_x,
                min_y - margin_y,
                max_y + margin_y,
            ]
            plt.imshow(img, extent=extent, aspect="auto", alpha=0.6, zorder=0)
        except Exception as e:
            print(f"Could not load background image: {e}")

    if weights:
        max_load = max(weights)
        norm_weights = [(w / max_load) * 7 + 1 for w in weights]
    else:
        norm_weights = 1

    nx.draw_networkx_edges(
        G, pos, edgelist=edges, width=norm_weights, edge_color="blue", alpha=0.6
    )

    nx.draw_networkx_nodes(
        G, pos, node_size=700, node_color="lightblue", edgecolors="black"
    )

    label_pos = {k: (v[0], v[1] + 0.15) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, font_size=14, font_weight="bold")

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=10,
        font_color="black",
        rotate=False,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.7),
    )

    plt.title(f"Network Traffic Load (m={modularity})", fontsize=16)
    plt.axis("off")
    plt.tight_layout()

    plots_dir = os.path.join(config.RESULTS_DIR, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    output_path = os.path.join(plots_dir, "map_visualization.png")

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
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    is_aggregation = not args.deagg
    mode_name = "Deaggregation" if args.deagg else "Aggregation"

    print(
        f"RUNNING MAP GENERATOR...\nMODULARITY: {args.modularity}, MODE: {mode_name}\n"
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
    visualize_network(args.file, best_chromosome, args.modularity, is_aggregation)
