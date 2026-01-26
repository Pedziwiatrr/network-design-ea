import argparse
import numpy as np
import json
import random
import time
import os
from src.utils.loader import SNDlibLoader
from src.ea import EvoSolver
from src import config


def main():
    global_start_time = time.time()

    parser = argparse.ArgumentParser(
        description="Evolutionary Algorithm for Network Design Problem",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input_file",
        type=str,
        default=config.DATA_FILE,
        help="Path to the input network data file.",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=config.DEFAULT_OUTPUT_NAME,
        help="Filename for the JSON results file.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=config.DEFAULT_REPEATS,
        help="Number of times to repeat the simulation for each configuration.",
    )
    parser.add_argument(
        "--pop",
        type=int,
        default=config.DEFAULT_POP_SIZE,
        help="Size of the population in each generation.",
    )
    parser.add_argument(
        "--gens",
        type=int,
        default=config.DEFAULT_GENERATIONS,
        help="Total number of generations to evolve.",
    )
    parser.add_argument(
        "--mutation_rate",
        type=float,
        default=config.DEFAULT_MUTATION_RATE,
        help="Probability of mutation for each gene.",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=config.DEFAULT_ALPHA,
        help="Crossover weighting factor (0.0-1.0).",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="all",
        choices=["all", "agg", "deagg"],
        help="Simulation mode: 'agg' (aggregation), 'deagg' (deaggregation), or 'all' (both).",
    )
    parser.add_argument(
        "--no_heuristic",
        action="store_true",
        default=not config.DEFAULT_USE_HEURISTIC,
        help="Disable initialization with heuristic solutions.",
    )
    parser.add_argument(
        "--heuristic_ratio",
        type=float,
        default=config.DEFAULT_HEURISTIC_RATIO,
        help="Ratio of the population initialized using heuristics (deterministic individual variants).",
    )
    parser.add_argument(
        "--no_elitism",
        action="store_true",
        default=not config.DEFAULT_ELITISM,
        help="Disable elitism (keeping the best individual).",
    )
    parser.add_argument(
        "--modularities",
        nargs="+",
        type=float,
        default=config.DEFAULT_MODULARITIES,
        help="List of modularity values to test.",
    )
    parser.add_argument(
        "--tournament_size",
        type=int,
        default=config.DEFAULT_TOURNAMENT_SIZE,
        help="Size of every tournament for selection.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Starting seed for random number generation (it will increment by 1 every simulation repetition).",
    )
    parser.add_argument(
        "--sigma",
        type=float,
        default=config.DEFAULT_SIGMA,
        help="Initial standard deviation for Gaussian mutation.",
    )
    args = parser.parse_args()

    try:
        base_seed = args.seed
        if args.seed is None:
            base_seed = random.randint(0, 20041202)

        network = SNDlibLoader.load(args.input_file)
        modularities = args.modularities

        if args.mode == "agg":
            modes = [True]
        elif args.mode == "deagg":
            modes = [False]
        else:
            modes = [True, False]

        print(
            f"\nREPEATS: {args.repeats}, POPULATION SIZE: {args.pop}, GENERATION COUNT: {args.gens}, MUTATION RATE: {args.mutation_rate}, SIGMA: {args.sigma},"
        )
        print(
            f"HEURISTIC RATIO: {args.heuristic_ratio}, MODE: {args.mode}, HEURISTIC: {not args.no_heuristic}, ELITISM: {not args.no_elitism}, TOURNAMENT SIZE: {args.tournament_size}"
        )
        print(f"STARTING SEED: {base_seed}")
        print("\n" + "=" * 130)
        print(
            f"{'Mode':<15} | {'Modularity':<15} | {'Best':<12} | {'Mean':<12} | {'Std Dev':<10} | {'Convergence Gen':<20} | {'Avg Time':<10}"
        )
        results_data = []

        for agg in modes:
            print("-" * 130)
            mode_label = "Aggregation" if agg else "Deaggregation"
            for m in modularities:
                seed = base_seed
                costs = []
                gens = []
                histories = []
                times = []

                best_chromosome_overall = None
                best_cost_overall = float("inf")

                for _ in range(args.repeats):
                    np.random.seed(seed)
                    random.seed(seed)
                    seed += 1

                    solver = EvoSolver(
                        network,
                        modularity=m,
                        aggregation=agg,
                        pop_size=args.pop,
                        generations=args.gens,
                        mutation_rate=args.mutation_rate,
                        alpha=args.alpha,
                        sigma=args.sigma,
                        use_heuristic=not args.no_heuristic,
                        heuristic_ratio=args.heuristic_ratio,
                        elitism=not args.no_elitism,
                        tournament_size=args.tournament_size,
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
                    f"{mode_label:<15} | {m:<15} | {np.min(costs):<12} | {np.mean(costs):<12.2f} | "
                    f"{np.std(costs):<10.2f} | {np.mean(gens):<20.1f} | {np.mean(times):.2f}s ({np.sum(times):.2f}s total)"
                )

        print("=" * 130)

        os.makedirs(config.RESULTS_DIR, exist_ok=True)
        final_path = os.path.join(config.RESULTS_DIR, args.output_file)
        if not final_path.endswith(".json"):
            final_path += ".json"

        with open(final_path, "w") as fh:
            json.dump(results_data, fh, indent=4)
        print(f"Results saved to {final_path}")

        global_end_time = time.time()
        print(
            f"Total execution time: {global_end_time - global_start_time:.2f} seconds"
        )

    except Exception as e:
        print(f"ERROR: {e} :(")


if __name__ == "__main__":
    main()
