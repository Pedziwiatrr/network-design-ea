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

    if not subset:
        print(f"No data found for modularity {target_modularity}")
        return

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

    output_path = os.path.join("results/plots", "convergence_plot.png")
    plt.savefig(output_path)
    print(f"Saved: {output_path}")


def plot_comparison_bar(data):
    if not data:
        return

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
    rects1 = plt.bar(x - width / 2, agg_costs, width, label="Aggregation")
    rects2 = plt.bar(x + width / 2, deagg_costs, width, label="Deaggregation")

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(
                rect.get_x() + rect.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )

    autolabel(rects1)
    autolabel(rects2)

    plt.xlabel("Modularity (m)")
    plt.ylabel("Minimum Cost (Log Scale)")
    plt.title("Cost Comparison: Aggregation vs Deaggregation")
    plt.xticks(x, modularities)
    plt.yscale("log")
    plt.legend()

    current_ylim = plt.ylim()
    plt.ylim(current_ylim[0], current_ylim[1] * 2)

    output_path = os.path.join("results/plots", "comparison_bar.png")
    plt.savefig(output_path)
    print(f"Saved: {output_path}")


def plot_time_complexity(data):
    plt.figure(figsize=(10, 6))

    modes = ["Aggregation", "Deaggregation"]
    modularities = sorted(list(set(d["modularity"] for d in data)))

    for mode in modes:
        times = []
        for m in modularities:
            val = next(
                (
                    d["avg_time"]
                    for d in data
                    if d["mode"] == mode and d["modularity"] == m
                ),
                0,
            )
            times.append(val)

        plt.plot(modularities, times, marker="o", linewidth=2, label=mode)

    plt.title("Computational Time vs Modularity")
    plt.xlabel("Modularity (m)")
    plt.ylabel("Average Time (seconds)")
    plt.xscale("log")
    plt.xticks(modularities, modularities)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()

    output_path = os.path.join("results/plots", "time_plot.png")
    plt.savefig(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    data = load_results()
    if data:
        plot_convergence(data, target_modularity=10)
        plot_comparison_bar(data)
        plot_time_complexity(data)
