import argparse
import numpy as np
import json
import time
import os
from src.loader import SNDlibLoader
from src.ea import EvoSolver
from src import config


def main():
    global_start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default=config.DATA_FILE)
    parser.add_argument("--repeats", type=int, default=config.DEFAULT_REPEATS)
    parser.add_argument("--pop", type=int, default=config.DEFAULT_POP_SIZE)
    parser.add_argument("--gens", type=int, default=config.DEFAULT_GENERATIONS)
    parser.add_argument(
        "--mutation_rate", type=float, default=config.DEFAULT_MUTATION_RATE
    )
    parser.add_argument("--alpha", type=float, default=config.DEFAULT_ALPHA)
    parser.add_argument(
        "--mode",
        type=str,
        default="all",
        choices=["all", "agg", "deagg"],
    )
    args = parser.parse_args()

    try:
        network = SNDlibLoader.load(args.file)
        modularities = config.DEFAULT_MODULARITIES

        if args.mode == "agg":
            modes = [True]
        elif args.mode == "deagg":
            modes = [False]
        else:
            modes = [True, False]

        print(
            f"\nREPEATS: {args.repeats}, POPULATION SIZE: {args.pop}, GENERATION COUNT: {args.gens}, MUTATION RATE: {args.mutation_rate}, MODE: {args.mode}"
        )
        print("=" * 130)
        print(
            f"{'Mode':<15} | {'Modularity':<15} | {'Best':<12} | {'Mean':<12} | {'Std Dev':<10} | {'Convergence Gen':<20} | {'Avg Time':<10}"
        )
        results_data = []

        for agg in modes:
            print("-" * 130)
            mode_label = "Aggregation" if agg else "Deaggregation"
            for m in modularities:
                costs = []
                gens = []
                histories = []
                times = []

                best_chromosome_overall = None
                best_cost_overall = float("inf")

                for _ in range(args.repeats):
                    solver = EvoSolver(
                        network,
                        modularity=m,
                        aggregation=agg,
                        pop_size=args.pop,
                        generations=args.gens,
                        mutation_rate=args.mutation_rate,
                        alpha=args.alpha,
                    )

                    start_time = time.time()
                    best_chrom, best, conv, history = solver.run()
                    end_time = time.time()

                    if best < best_cost_overall:
                        best_cost_overall = best
                        best_chromosome_overall = best_chrom

                    costs.append(best)
                    gens.append(conv)
                    histories.append(history)
                    times.append(end_time - start_time)

                results_data.append(
                    {
                        "mode": mode_label,
                        "modularity": m,
                        "best_cost": float(np.min(costs)),
                        "mean_cost": float(np.mean(costs)),
                        "std_cost": float(np.std(costs)),
                        "avg_convergence": float(np.mean(gens)),
                        "avg_time": float(np.mean(times)),
                        "histories": histories[0],
                        "best_chromosome": best_chromosome_overall.tolist()
                        if best_chromosome_overall is not None
                        else [],
                    }
                )

                print(
                    f"{mode_label:<15} | {m:<15} | {np.min(costs):<12} | {np.mean(costs):<10.2f} | "
                    f"{np.std(costs):<10.2f} | {np.mean(gens):<20.1f} | {np.mean(times):.2f}s ({np.sum(times):.2f}s total)"
                )

        print("=" * 130)

        os.makedirs(config.RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(config.RESULTS_DIR, "results.json")

        with open(output_file, "w") as fh:
            json.dump(results_data, fh, indent=4)
        print(f"Results saved to {output_file}")

        global_end_time = time.time()
        print(
            f"Total execution time: {global_end_time - global_start_time:.2f} seconds"
        )

    except Exception as e:
        print(f"ERROR: {e} :(")


if __name__ == "__main__":
    main()
