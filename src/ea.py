import numpy as np
import random
import math
from copy import deepcopy
from .models import Network

# 🧬🧬🧬
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

    def get_link_loads(self):
        link_loads = {lid: 0.0 for lid in self.network.links}

        for i, d_id in enumerate(self.demand_ids):
            demand = self.network.demands[d_id]
            paths = demand.admissable_paths
            num_paths = len(paths)

            if num_paths == 0:
                continue

            # connecting weights to admissable paths
            weights = individual[i, :num_paths]

            # Aggregation - Winner takes all >:) 🤑 🎩
            if self.aggregation:
                chosen_idx = np.argmax(weight)
                chosen_path = paths[chosen_idx]
                for link_id in chosen_path:
                    link_loads[link_id] += demand.value

            # Deaggregation - Flow proportional to weights ☭ 🫱🏻‍🫲🏼
            else:
                total_weight = np.sum(weights)
                ratios = weights / total_w

                for idx, ratio in enumerate(ratios):
                    flow = demand.value * ratio
                    path = paths[idx]
                    for link_id in path:
                        link_loads[link_id] += flow

        return link_loads

    def selection(self, scores, k):
        #TODO: selection tournament
        pass

    def crossover(self, first, second):
        #TODO: arythmetic avg parent's values
        pass

    def mutation(self, individual):
        #TODO: gaussian mutation
        pass

    def run(self):
        """
        Main evolution loop.
        """

        for gen in range(self.generations):
            scores = [self.calculate_cost(individual) for individual in self.population]

            min_cost = min(scores)
            if min_cost < best_global_cost:
                best_global_cost = min_cost

            new_population = []
            while len(new_population) < self.pop_size:
                pass
                #TODO: selection, mutation, crossovers etc. Making new generation.

            #TODO: finishing the function with the rest of new gen's creation.

        return best_global_cost