import os
import argparse
import numpy as np
from src.loader import SNDlibLoader
from src.ea import EvoSolver

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument('--nodes', action='store_true')
    parser.add_argument('--links', action='store_true')
    parser.add_argument('--demands', action='store_true')
    parser.add_argument('--test_solver', action='store_true')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--file', type=str, default=os.path.join(base_dir, 'data', 'polska.txt'))
    args = parser.parse_args()

    try:
        print(f"Loading data from {args.file}")
        network = SNDlibLoader.load(args.file)

        if args.nodes or args.all:
            print("="*100)
            print(f"> Node count: {len(network.nodes)}")
            print("-" * 50)
            for node in network.nodes.values():
                print(f"ID: {node.id:<12} X: {node.x:<8} Y: {node.y}")

        if args.links or args.all:
            print("="*100)
            print(f"> Link count: {len(network.links)}")
            print("-" * 50)
            for link in network.links.values():
                print(f"ID: {link.id:<12} Src: {link.source:<12} -> Tgt: {link.target:<12}")

        if args.demands or args.all:
            print("="*100)
            print(f"> Demand count: {len(network.demands)}")
            print("-" * 50)
            for demand in network.demands.values():
                print(f"Demand: {demand.id}")
                print(f"    Route: {demand.source} -> {demand.target}")
                print(f"    Value: {demand.value}")
                print(f"    Admissible paths count: {len(demand.admissable_paths)}")
                print(f"    Admissable paths:")
                for i, path in enumerate(demand.admissable_paths):
                     print(f"   {i}: {path}")
                print("-" * 50)

        if args.test_solver or args.all:
            print()
            print("="*100)
            print("< Testing evolutionary solver >\n")
            solver = EvoSolver(network, modularity=1.0, aggregation=True)

            num_demands = len(solver.demand_ids)
            max_paths = max(len(d.admissable_paths) for d in network.demands.values())

            test_individual = np.random.rand(num_demands, max_paths)
            test_individual_2 = np.random.rand(num_demands, max_paths)

            print("-" * 50)
            print(" test get_link_loads:")
            loads = solver.get_link_loads(test_individual)
            print(f" all loads: {loads}")
            total_load = sum(loads.values())
            print(f" total load in network: {total_load:.2f}")

            print("-" * 50)
            print(" test calculate_cost:")
            cost = solver.calculate_cost(test_individual)
            print(f" calculated cost: {cost}")
            print("-" * 50)

            print(" test crossover")
            child = solver.crossover(test_individual, test_individual_2)
            print(f" crossover child: {child} ")
            print("="*100)

        print("finito")

    except Exception as e:
        print(f"ERROR! : {e} :(")

if __name__ == "__main__":
    main()