import os
from src.loader import SNDlibLoader

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', 'polska.txt')

    try:
        print(f"Loading data from {file_path}")
        network = SNDlibLoader.load(file_path)

        print("="*100)

        # NODES
        print(f"> Node count: {len(network.nodes)}")
        print("-" * 50)
        for node in network.nodes.values():
            print(f"ID: {node.id:<12} X: {node.x:<8} Y: {node.y}")

        print("="*100)

        # LINKS
        print(f"> Link count: {len(network.links)}")
        print("-" * 50)
        for link in network.links.values():
            print(f"ID: {link.id:<12} Src: {link.source:<12} -> Tgt: {link.target:<12} Cost: {link.cost}")

        print("="*100)

        # DEMANDS
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