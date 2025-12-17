import os
import argparse
from src.loader import SNDlibLoader

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument('--nodes', action='store_true')
    parser.add_argument('--links', action='store_true')
    parser.add_argument('--demands', action='store_true')
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
                print(f"ID: {link.id:<12} Src: {link.source:<12} -> Tgt: {link.target:<12} Cost: {link.cost}")

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

    except Exception as e:
        print(f"ERROR! : {e} :(")

if __name__ == "__main__":
    main()