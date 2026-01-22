import numpy as np
import random
import math
from copy import deepcopy
from .models import Network


class EvoSolver:
    def __init__(
        self,
        network: Network,
        modularity: float = 1.0,
        aggregation: bool = True,
        pop_size: int = 100,
        generations: int = 100,
        mutation_rate: float = 0.1,
        alpha: float = 0.5,
    ):
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
        """
        Calculates total traffic load for each link in the network.

        Implements two scenarios:
        - aggregation: traffic follows the path with the highest weight (not splitted).
        - deaggregation: traffic distributed proportionally among all paths (splitted).
        """
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

                if total_weight > 0:
                    ratios = weights / total_weight
                else:
                    ratios = np.ones(num_paths) / num_paths

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
            total_cost += math.ceil(round(load, 6) / self.modularity)
        return total_cost

    def initialize_population(self):
        """Initialize population with 1 deterministic individual and the rest generated randomly"""
        self.population = []

        num_demands = len(self.demand_ids)
        max_paths = max(
            len(self.network.demands[demand_id].admissable_paths)
            for demand_id in self.demand_ids
        )

        # deterministic - 1 individual
        deterministic_individual = np.zeros((num_demands, max_paths))
        for i, demand_id in enumerate(self.demand_ids):
            paths = self.network.demands[demand_id].admissable_paths
            shortest_path_idx = np.argmin([len(p) for p in paths])
            deterministic_individual[i, shortest_path_idx] = 1.0

        self.population.append(deterministic_individual)

        # random - the rest
        for i in range(self.pop_size - 1):
            random_individual = np.random.rand(num_demands, max_paths)
            self.population.append(random_individual)

    def selection(self, scores, k=3):
        """tournament selection"""
        selected = random.sample(range(len(self.population)), k)
        best_idx = selected[0]
        for idx in selected:
            if scores[idx] < scores[best_idx]:
                best_idx = idx

        return deepcopy(self.population[best_idx])

    def crossover(self, first, second):
        """arithmetic crossover: descendant weights based on parent's weights linear combination"""
        return self.alpha * first + (1 - self.alpha) * second

    def mutation(self, individual):
        """gaussian mutation"""
        mask = np.random.rand(*individual.shape) < self.mutation_rate
        noise = np.random.normal(0, 0.2, individual.shape)
        individual[mask] += noise[mask]
        np.clip(individual, 0.0, 1.0, out=individual)

    def run(self):
        """Main evolution loop."""

        self.initialize_population()
        best_global_cost = float("inf")
        last_improvement_gen = 0
        best_costs_history = []
        best_chromosome = None

        for gen in range(self.generations):
            scores = [self.calculate_cost(individual) for individual in self.population]

            min_idx = np.argmin(scores)
            min_cost = scores[min_idx]

            if min_cost < best_global_cost:
                best_global_cost = min_cost
                best_chromosome = deepcopy(self.population[min_idx])
                last_improvement_gen = gen

            best_costs_history.append(best_global_cost)

            new_population = [deepcopy(self.population[min_idx])]

            while len(new_population) < self.pop_size:
                parent1 = self.selection(scores)
                parent2 = self.selection(scores)

                child = self.crossover(parent1, parent2)
                self.mutation(child)

                new_population.append(child)

            self.population = new_population

        return (
            best_chromosome,
            best_global_cost,
            last_improvement_gen,
            best_costs_history,
        )
