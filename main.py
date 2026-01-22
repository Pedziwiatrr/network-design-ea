import os
import argparse
import numpy as np
import json
from src.loader import SNDlibLoader
from src.ea import EvoSolver


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", type=str, default=os.path.join(base_dir, "data", "polska.txt")
    )
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--pop", type=int, default=300)
    parser.add_argument("--gens", type=int, default=300)
    parser.add_argument("--mutation_rate", type=float, default=0.1)
    parser.add_argument("--alpha", type=float, default=0.5)
    args = parser.parse_args()

    try:
        network = SNDlibLoader.load(args.file)
        modularities = [1, 10, 100, 1000]
        scenarios = [True, False]

        print("\n" + "=" * 110)
        print(
            f"{'Mode':<15} | {'Modularity':<15} | {'Best':<12} | {'Mean':<10} | {'Standard Deviation':<20} | {'Last improvement gen':<30}"
        )
        print("-" * 110)

        results_data = []

        for agg in scenarios:
            mode_label = "Aggregation" if agg else "Deaggregation"
            for m in modularities:
                costs = []
                gens = []
                histories = []

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
                    best, conv, history = solver.run()

                    costs.append(best)
                    gens.append(conv)
                    histories.append(history)

                results_data.append(
                    {
                        "mode": mode_label,
                        "modularity": m,
                        "best_cost": float(np.min(costs)),
                        "mean_cost": float(np.mean(costs)),
                        "std_cost": float(np.std(costs)),
                        "avg_convergence": float(np.mean(gens)),
                        "histories": histories[0],
                    }
                )

                print(
                    f"{mode_label:<15} | {m:<15} | {np.min(costs):<12} | {np.mean(costs):<10.2f} | "
                    f"{np.std(costs):<20.2f} | {np.mean(gens):<30.1f}"
                )

        print("=" * 110)

        os.makedirs("results", exist_ok=True)
        with open("results/results.json", "w") as fh:
            json.dump(results_data, fh, indent=4)
    except Exception as e:
        print(f"ERROR: {e} :(")


if __name__ == "__main__":
    main()
