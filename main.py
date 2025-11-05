import network
import ga_aggregation
import ga_deaggregation
import time

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.8
TOURNAMENT_SIZE = 3

MODULARITY_M = 10.0

AGGREGATION_MODE = True


def main():
    print(f"Starting EA for network optimization")
    print(f"Mode: {'Aggregation' if AGGREGATION_MODE else 'Deaggregation'}")
    print(f"Modularity (m): {MODULARITY_M}")
    print(f"Population: {POPULATION_SIZE}, Generations: {GENERATIONS}")
    print(f"Mutation: {MUTATION_RATE}, Crossover: {CROSSOVER_RATE}")

    net_data = network.get_network_data()

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
    print(f"Best solution (chromosome):")
    print(best_individual['chromosome'])


if __name__ == "__main__":
    main()