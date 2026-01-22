import os
import argparse
import numpy as np
from src.utils.loader import SNDlibLoader
from src.ea import EvoSolver


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_solver", action="store_true")
    parser.add_argument("--test_loading", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument(
        "--file", type=str, default=os.path.join(base_dir, "data", "polska.txt")
    )
    args = parser.parse_args()

    try:
        print(f"Loading data from {args.file}")
        network = SNDlibLoader.load(args.file)

        if args.test_loading or args.all:
            print("=" * 100)
            print(f"> Node count: {len(network.nodes)}")
            print("-" * 50)
            for node in network.nodes.values():
                print(f"ID: {node.id:<12} X: {node.x:<8} Y: {node.y}")
            print("=" * 100)
            print(f"> Link count: {len(network.links)}")
            print("-" * 50)
            for link in network.links.values():
                print(
                    f"ID: {link.id:<12} Src: {link.source:<12} -> Tgt: {link.target:<12}"
                )
            print("=" * 100)
            print(f"> Demand count: {len(network.demands)}")
            print("-" * 50)
            for demand in network.demands.values():
                print(
                    f"Demand: {demand.id} | Route: {demand.source} -> {demand.target} | Value: {demand.value}"
                )

        if args.test_solver or args.all:
            print("\n" + "=" * 100)
            print("< Testing evolutionary solver functions >\n")
            solver = EvoSolver(network, modularity=1.0, aggregation=True)
            d_count = len(solver.demand_ids)
            k_max = max(len(d.admissable_paths) for d in network.demands.values())

            ind1 = np.random.rand(d_count, k_max)
            ind2 = np.random.rand(d_count, k_max)

            print("-" * 50)
            loads = solver.get_link_loads(ind1)
            print(f"Total network load: {sum(loads.values()):.2f}")

            print("-" * 50)
            cost = solver.calculate_cost(ind1)
            print(f"Current cost: {cost}")

            print("-" * 50)
            child = solver.crossover(ind1, ind2)
            solver.mutation(child)
            print(f"Mutated child created by crossover: {child}")
            # print(f"\nind1: {ind1}, \n\n ind2:{ind2}\n")

            print("-" * 50)
            print("Running full EA test (short):")
            solver.generations = 5
            best_cost, last_improvement_gen = solver.run()
            print(
                f"Result: Cost {best_cost}, Last improvement in gen: {last_improvement_gen}"
            )
            print("=" * 100)

        print("finito")

    except Exception as e:
        print(f"ERROR! : {e} :(")


if __name__ == "__main__":
    main()
