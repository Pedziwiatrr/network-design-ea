import numpy as node_pattern
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

    def get_link_loads(self):
        link_loads = {lid: 0.0 for lid in self.network.links}
        pass



