import network
import ga_aggregation
import ga_deaggregation
import time
import os

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.8
TOURNAMENT_SIZE = 3

MODULARITY_M = 10.0

AGGREGATION_MODE = True

OUTPUT_DIR = "results"


def main():
    print(f"Starting EA for network optimization")
    print(f"Mode: {'Aggregation' if AGGREGATION_MODE else 'Deaggregation'}")
    print(f"Modularity (m): {MODULARITY_M}")
    print(f"Population: {POPULATION_SIZE}, Generations: {GENERATIONS}")
    print(f"Mutation: {MUTATION_RATE}, Crossover: {CROSSOVER_RATE}")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    net_data = network.get_network_data()

    topo_filename = os.path.join(OUTPUT_DIR, "network_topology.png")
    network.visualize_network(net_data, topo_filename)
    print(f"\nBase network topology saved to {topo_filename}")

    start_time = time.time()

    if AGGREGATION_MODE:
        best_individual = ga_aggregation.run_ea(
            network_data=net_data,
            modularity_m=MODULARITY_M,
            pop_size=POPULATION_SIZE,
            generations=GENERATIONS,
            crossover_rate=CROSSOVER_RATE,
            mutation_rate=MUTATION_RATE,
            tournament_size=TOURNAMENT_SIZE
        )
    else:
        best_individual = ga_deaggregation.run_ea(
            network_data=net_data,
            modularity_m=MODULARITY_M,
            pop_size=POPULATION_SIZE,
            generations=GENERATIONS,
            crossover_rate=CROSSOVER_RATE,
            mutation_rate=MUTATION_RATE,
            tournament_size=TOURNAMENT_SIZE
        )

    end_time = time.time()

    print(f"\nCalculations finished in {end_time - start_time:.2f} s")
    print(f"Best found cost (fitness): {best_individual['fitness']}")

    base_solution_fn = f"solution_{'agg' if AGGREGATION_MODE else 'deagg'}_m{MODULARITY_M}.png"
    solution_filename = os.path.join(OUTPUT_DIR, base_solution_fn)

    network.visualize_solution(
        net_data,
        best_individual,
        MODULARITY_M,
        AGGREGATION_MODE,
        solution_filename
    )
    print(f"Solution graph saved to {solution_filename}")


if __name__ == "__main__":
    main()