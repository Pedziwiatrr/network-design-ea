import random
import math
import copy


def calculate_fitness(chromosome, network_data, modularity_m):
    edge_loads = {edge: 0 for edge in network_data['edges']}

    for i, demand in enumerate(network_data['demands']):
        chosen_path_index = chromosome[i]
        chosen_path = network_data['paths'][demand['id']][chosen_path_index]
        demand_value = demand['value']

        for edge in chosen_path:
            found_edge = None
            for net_edge in network_data['edges']:
                if net_edge == edge:
                    found_edge = net_edge
                    break

            if found_edge in edge_loads:
                edge_loads[found_edge] += demand_value
            else:
                pass

    total_cost = 0
    for load in edge_loads.values():
        if load > 0:
            total_cost += math.ceil(load / modularity_m)

    return total_cost


def create_individual(network_data):
    chromosome = []
    for demand in network_data['demands']:
        num_paths = len(network_data['paths'][demand['id']])
        chromosome.append(random.randint(0, num_paths - 1))
    return {'chromosome': chromosome, 'fitness': float('inf')}


def initialize_population(pop_size, network_data):
    population = []
    for _ in range(pop_size):
        individual = create_individual(network_data)
        population.append(individual)
    return population


def selection(population, tournament_size):
    tournament = random.sample(population, tournament_size)
    best = min(tournament, key=lambda x: x['fitness'])
    return best


def crossover(parent1, parent2):
    p1_chrom = parent1['chromosome']
    p2_chrom = parent2['chromosome']

    size = len(p1_chrom)
    if size < 2:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    crossover_point = random.randint(1, size - 1)

    child1_chrom = p1_chrom[:crossover_point] + p2_chrom[crossover_point:]
    child2_chrom = p2_chrom[:crossover_point] + p1_chrom[crossover_point:]

    child1 = {'chromosome': child1_chrom, 'fitness': float('inf')}
    child2 = {'chromosome': child2_chrom, 'fitness': float('inf')}

    return child1, child2


def mutate(individual, mutation_rate, network_data):
    chromosome = individual['chromosome']
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            demand_id = network_data['demands'][i]['id']
            num_paths = len(network_data['paths'][demand_id])

            if num_paths > 1:
                new_path_index = random.randint(0, num_paths - 1)
                while new_path_index == chromosome[i]:
                    new_path_index = random.randint(0, num_paths - 1)
                chromosome[i] = new_path_index

    return individual


def run_ea(network_data, modularity_m, pop_size, generations, crossover_rate, mutation_rate, tournament_size):
    population = initialize_population(pop_size, network_data)
    for ind in population:
        ind['fitness'] = calculate_fitness(ind['chromosome'], network_data, modularity_m)

    best_overall = min(population, key=lambda x: x['fitness'])

    for gen in range(generations):
        new_population = []

        elitism_count = int(pop_size * 0.1)
        sorted_pop = sorted(population, key=lambda x: x['fitness'])
        new_population.extend(sorted_pop[:elitism_count])

        while len(new_population) < pop_size:
            parent1 = selection(population, tournament_size)
            parent2 = selection(population, tournament_size)

            child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)

            child1 = mutate(child1, mutation_rate, network_data)
            child2 = mutate(child2, mutation_rate, network_data)

            child1['fitness'] = calculate_fitness(child1['chromosome'], network_data, modularity_m)
            child2['fitness'] = calculate_fitness(child2['chromosome'], network_data, modularity_m)

            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)

        population = new_population
        best_in_gen = min(population, key=lambda x: x['fitness'])

        if best_in_gen['fitness'] < best_overall['fitness']:
            best_overall = copy.deepcopy(best_in_gen)

        if (gen + 1) % 10 == 0:
            print(f"Generation {gen + 1}/{generations} | Best cost: {best_overall['fitness']:.2f}")

    return best_overall