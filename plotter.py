import json
import matplotlib.pyplot as plt
import numpy as np
import os


def load_results(filename="results/results.json"):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return []
    with open(filename, "r") as f:
        return json.load(f)


def plot_convergence(data, target_modularity=10):
    plt.figure(figsize=(10, 6))

    subset = [d for d in data if d["modularity"] == target_modularity]

    for item in subset:
        plt.plot(
            item["histories"],
            label=f"{item['mode']} (m={target_modularity})",
            linewidth=2,
        )

    plt.title(f"Convergence (Cost vs Generation) for m={target_modularity}")
    plt.xlabel("Generation")
    plt.ylabel("Best Cost")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()

    output_path = os.path.join("results", "convergence_plot.png")
    plt.savefig(output_path)
    print(f"Saved: {output_path}")


def plot_comparison_bar(data):
    modes = ["Aggregation", "Deaggregation"]
    modularities = sorted(list(set(d["modularity"] for d in data)))

    agg_costs = []
    deagg_costs = []

    for m in modularities:
        agg_val = next(
            (
                d["best_cost"]
                for d in data
                if d["mode"] == "Aggregation" and d["modularity"] == m
            ),
            0,
        )
        deagg_val = next(
            (
                d["best_cost"]
                for d in data
                if d["mode"] == "Deaggregation" and d["modularity"] == m
            ),
            0,
        )
        agg_costs.append(agg_val)
        deagg_costs.append(deagg_val)

    x = np.arange(len(modularities))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, agg_costs, width, label="Aggregation")
    plt.bar(x + width / 2, deagg_costs, width, label="Deaggregation")

    plt.xlabel("Modularity (m)")
    plt.ylabel("Minimum Cost (Log Scale)")
    plt.title("Cost Comparison: Aggregation vs Deaggregation")
    plt.xticks(x, modularities)
    plt.yscale("log")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5, which="both")

    output_path = os.path.join("results", "comparison_bar.png")
    plt.savefig(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    data = load_results()
    if data:
        plot_convergence(data, target_modularity=10)
        plot_comparison_bar(data)
