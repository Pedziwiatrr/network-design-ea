import random
import math
import copy


def _normalize_ratios(ratios):
    total = sum(ratios)
    if total == 0:
        return [1.0 / len(ratios)] * len(ratios)
    return [r / total for r in ratios]


def calculate_fitness(chromosome, network_data, modularity_m):
    edge_loads = {edge: 0 for edge in network_data['edges']}

    for i, demand in enumerate(network_data['demands']):
        path_ratios = chromosome[i]
        demand_value = demand['value']
        available_paths = network_data['paths'][demand['id']]

        for path_index, ratio in enumerate(path_ratios):
            flow_on_path = demand_value * ratio
            path = available_paths[path_index]
            for edge in path:
                found_edge = None
                for net_edge in network_data['edges']:
                    if net_edge == edge:
                        found_edge = net_edge
                        break

                if found_edge in edge_loads:
                    edge_loads[found_edge] += flow_on_path
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
        ratios = [random.random() for _ in range(num_paths)]
        chromosome.append(_normalize_ratios(ratios))
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

    alpha = random.random()

    child1_chrom = []
    child2_chrom = []

    for p1_ratios, p2_ratios in zip(p1_chrom, p2_chrom):
        c1_ratios = []
        c2_ratios = []
        for r1, r2 in zip(p1_ratios, p2_ratios):
            c1_r = alpha * r1 + (1.0 - alpha) * r2
            c2_r = (1.0 - alpha) * r1 + alpha * r2
            c1_ratios.append(c1_r)
            c2_ratios.append(c2_r)

        child1_chrom.append(_normalize_ratios(c1_ratios))
        child2_chrom.append(_normalize_ratios(c2_ratios))

    child1 = {'chromosome': child1_chrom, 'fitness': float('inf')}
    child2 = {'chromosome': child2_chrom, 'fitness': float('inf')}

    return child1, child2


def mutate(individual, mutation_rate, network_data):
    chromosome = individual['chromosome']
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            ratios = chromosome[i]
            if len(ratios) > 1:
                new_ratios = [max(0.0, r + random.gauss(0, 0.1)) for r in ratios]
                chromosome[i] = _normalize_ratios(new_ratios)
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