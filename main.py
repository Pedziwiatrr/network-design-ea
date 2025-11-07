import network
import ga_aggregation
import ga_deaggregation
import time
import os
import argparse


def main(agg_mode, mod_m, pop_size, gens, mut_rate, cross_rate, tourn_size, out_dir):
    print(f"Starting EA for network optimization")
    print(f"Mode: {'Aggregation' if agg_mode else 'Deaggregation'}")
    print(f"Modularity (m): {mod_m}")
    print(f"Population: {pop_size}, Generations: {gens}")
    print(f"Mutation: {mut_rate}, Crossover: {cross_rate}")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print(f"Created output directory: {out_dir}")

    net_data = network.get_network_data()

    topo_filename = os.path.join(out_dir, "network_topology.png")
    network.visualize_network(net_data, topo_filename)
    print(f"\nBase network topology saved to {topo_filename}")

    start_time = time.time()

    if agg_mode:
        best_individual = ga_aggregation.run_ea(
            network_data=net_data,
            modularity_m=mod_m,
            pop_size=pop_size,
            generations=gens,
            crossover_rate=cross_rate,
            mutation_rate=mut_rate,
            tournament_size=tourn_size
        )
    else:
        best_individual = ga_deaggregation.run_ea(
            network_data=net_data,
            modularity_m=mod_m,
            pop_size=pop_size,
            generations=gens,
            crossover_rate=cross_rate,
            mutation_rate=mut_rate,
            tournament_size=tourn_size
        )

    end_time = time.time()

    print(f"\nCalculations finished in {end_time - start_time:.2f} s")
    print(f"Best found cost (fitness): {best_individual['fitness']}")

    base_solution_fn = f"solution_{'agg' if agg_mode else 'deagg'}_m{mod_m}.png"
    solution_filename = os.path.join(out_dir, base_solution_fn)

    network.visualize_solution(
        net_data,
        best_individual,
        mod_m,
        agg_mode,
        solution_filename
    )
    print(f"Solution graph saved to {solution_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Evolutionary Algorithm for Network Optimization")

    parser.add_argument('--mode', type=str, choices=['aggregation', 'deaggregation'], default='aggregation',
                        help="Set the EA mode (default: aggregation).")
    parser.add_argument('-m', '--modularity', type=float, default=10.0,
                        help="Modularity (m) for cost calculation (default: 10.0).")
    parser.add_argument('-p', '--population', type=int, default=50, help="Population size (default: 50).")
    parser.add_argument('-g', '--generations', type=int, default=100, help="Number of generations (default: 100).")
    parser.add_argument('--mutation', type=float, default=0.05, help="Mutation rate (default: 0.05).")
    parser.add_argument('--crossover', type=float, default=0.8, help="Crossover rate (default: 0.8).")
    parser.add_argument('--tournament', type=int, default=3, help="Tournament size for selection (default: 3).")
    parser.add_argument('-o', '--output', type=str, default="results",
                        help="Output directory for graphs (default: 'results').")

    args = parser.parse_args()

    aggregation_mode = (args.mode == 'aggregation')

    main(
        agg_mode=aggregation_mode,
        mod_m=args.modularity,
        pop_size=args.population,
        gens=args.generations,
        mut_rate=args.mutation,
        cross_rate=args.crossover,
        tourn_size=args.tournament,
        out_dir=args.output
    )