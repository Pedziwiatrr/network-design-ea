import os

# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "polska.txt")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# EA PARAMETERS
DEFAULT_POP_SIZE = 300
DEFAULT_GENERATIONS = 100
DEFAULT_MUTATION_RATE = 0.5
DEFAULT_ALPHA = 0.5
DEFAULT_MODULARITIES = [1, 10, 100, 1000]
DEFAULT_USE_HEURISTIC = True

# META PARAMETERS
DEFAULT_REPEATS = 10
DEFAULT_MODULARITY = 10  # For visualization only
