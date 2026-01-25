import json
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse


def load_results(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return []
    with open(filename, "r") as f:
        return json.load(f)


def ensure_plot_dir(directory="results/plots"):
    if not os.path.exists(directory):
        os.makedirs(directory)


def plot_convergence(data):
    modularities = sorted(list(set(d["modularity"] for d in data)))

    if not modularities:
        print("No data found to plot convergence.")
        return

    num_plots = len(modularities)
    cols = 2
    rows = (num_plots + 1) // 2

    fig, axes = plt.subplots(rows, cols, figsize=(14, 5 * rows))

    if num_plots > 1:
        axes_flat = axes.flatten()
    else:
        axes_flat = [axes]

    ensure_plot_dir()

    for i, m in enumerate(modularities):
        ax = axes_flat[i]
        subset = [d for d in data if d["modularity"] == m]

        subset.sort(key=lambda x: x["mode"])

        for item in subset:
            ax.plot(
                item["histories"],
                label=f"{item['mode']}",
                linewidth=2,
            )

        ax.set_title(f"Convergence (m={int(m)})")
        ax.set_xlabel("Generation")
        ax.set_ylabel("Best Cost")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()

    for j in range(num_plots, len(axes_flat)):
        fig.delaxes(axes_flat[j])

    plt.tight_layout()
    output_path = os.path.join("results/plots", "convergence_all.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_comparison_bar(data):
    if not data:
        return

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
            if height > 0:
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

    ensure_plot_dir()
    output_path = os.path.join("results/plots", "comparison_bar.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_time_complexity(data):
    plt.figure(figsize=(10, 6))

    modes = ["Aggregation", "Deaggregation"]
    if not data:
        return
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

    ensure_plot_dir()
    output_path = os.path.join("results/plots", "time_plot.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        type=str,
        default="results/results.json",
    )
    args = parser.parse_args()

    data = load_results(args.file)
    if data:
        plot_convergence(data)
        plot_comparison_bar(data)
        plot_time_complexity(data)
