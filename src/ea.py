import numpy as np
import random
import math
from copy import deepcopy
from .models import Network


class EvoSolver:
    def __init__(self, network: Network, modularity: float = 1.0, aggregation: bool = True,
                 pop_size: int = 100, generations: int = 100, mutation_rate: float = 0.1, alpha: float = 0.5):
        self.network = network
        self.modularity = modularity
        self.aggregation = aggregation
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.alpha = alpha
        self.population = []
        self.demand_ids = list(network.demands.keys())

    def get_link_loads(self, individual):
        link_loads = {lid: 0.0 for lid in self.network.links}

        for i, d_id in enumerate(self.demand_ids):
            demand = self.network.demands[d_id]
            paths = demand.admissable_paths
            num_paths = len(paths)

            if num_paths == 0:
                continue

            # connecting weights to admissable paths
            weights = individual[i, :num_paths]

            # Aggregation - Winner takes all
            if self.aggregation:
                chosen_idx = np.argmax(weights)
                chosen_path = paths[chosen_idx]
                for link_id in chosen_path:
                    link_loads[link_id] += demand.value

            # Deaggregation - Flow proportional to weights
            else:
                total_weight = np.sum(weights)
                ratios = weights / total_weight

                for idx, ratio in enumerate(ratios):
                    flow = demand.value * ratio
                    path = paths[idx]
                    for link_id in path:
                        link_loads[link_id] += flow

        return link_loads

    def calculate_cost(self, individual):
        loads = self.get_link_loads(individual)
        total_cost = 0
        for load in loads.values():
            total_cost += math.ceil(load / self.modularity)
        return total_cost

    def initialize_population(self):
        """ Initialize population with 1 deterministic individual and the rest generated randomly """
        self.population = []

        num_demands = len(self.demand_ids)
        max_paths = max(len(self.network.demands[demand_id].admissable_paths) for demand_id in self.demand_ids)

        # deterministic - 1 individual
        deterministic_individual = np.zeros((num_demands, max_paths))
        for i, demand_id in enumerate(self.demand_ids):
            paths = self.network.demands[demand_id].admissable_paths
            shortest_path_idx = np.argmin([len(p) for p in paths])
            deterministic_individual[i, shortest_path_idx] = 1.0

        self.population.append(deterministic_individual)

        # random - the rest
        for i in range(self.pop_size - 1):
            random_individual  = np.random.rand(num_demands, max_paths)
            self.population.append(random_individual)


    def selection(self, scores, k):
        #TODO: selection tournament
        pass

    def crossover(self, first, second):
        """ arithmetic crossover: descendant weights based on parent's weights linear combination """
        return self.alpha * first + (1 - self.alpha) * second

    def mutation(self, individual):
        #TODO: gaussian mutation
        pass

    def run(self):
        """ Main evolution loop. """

        self.initialize_population()
        best_global_cost = float('inf')

        for gen in range(self.generations):
            scores = [self.calculate_cost(individual) for individual in self.population]

            min_cost = min(scores)
            if min_cost < best_global_cost:
                best_global_cost = min_cost

            new_population = []
            #while len(new_population) < self.pop_size:
                #pass
                #TODO: selection, mutation, crossovers etc. Making new generation.

            #TODO: finishing the function with the rest of new gen's creation.

        return best_global_cost