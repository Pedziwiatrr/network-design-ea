import os
import argparse
import numpy as np
import json
import time
from src.loader import SNDlibLoader
from src.ea import EvoSolver


def main():
    global_start_time = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", type=str, default=os.path.join(base_dir, "data", "polska.txt")
    )
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--pop", type=int, default=300)
    parser.add_argument("--gens", type=int, default=100)
    parser.add_argument("--mutation_rate", type=float, default=0.5)
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument(
        "--scenario",
        type=str,
        default="all",
        choices=["all", "agg", "deagg"],
    )
    args = parser.parse_args()

    try:
        network = SNDlibLoader.load(args.file)
        modularities = [1, 10, 100, 1000]

        if args.scenario == "agg":
            scenarios = [True]
        elif args.scenario == "deagg":
            scenarios = [False]
        else:
            scenarios = [True, False]

        print(
            f"\nREPEATS: {args.repeats}, POPULATION SIZE: {args.pop}, GENERATION COUNT: {args.gens}, MUTATION RATE: {args.mutation_rate}, SCENARIO: {args.scenario}"
        )
        print("=" * 130)
        print(
            f"{'Mode':<15} | {'Modularity':<15} | {'Best':<12} | {'Mean':<10} | {'Std Dev':<10} | {'Convergence Gen':<20} | {'Avg Time':<10}"
        )
        results_data = []

        for agg in scenarios:
            print("-" * 130)
            mode_label = "Aggregation" if agg else "Deaggregation"
            for m in modularities:
                costs = []
                gens = []
                histories = []
                times = []

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
                    best, conv, history = solver.run()
                    end_time = time.time()

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
                    }
                )

                print(
                    f"{mode_label:<15} | {m:<15} | {np.min(costs):<12} | {np.mean(costs):<10.2f} | "
                    f"{np.std(costs):<10.2f} | {np.mean(gens):<20.1f} | {np.mean(times):.4f}s ({np.sum(times):.2f}s total)"
                )

        print("=" * 130)

        os.makedirs("results", exist_ok=True)
        output_file = "results/results.json"

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
