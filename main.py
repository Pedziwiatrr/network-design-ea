import os
from src.loader import SNDlibLoader


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', 'polska.txt')

    try:
        print(f"Loading data from {file_path}")

        network = SNDlibLoader.load(file_path)

        print("="*100)
        print(f"> Node count: {len(network.nodes)}")
        print(f"> Link count: {len(network.nodes)}")
        print(f"> Demand count: {len(network.demands)}")

    except Exception as e:
        print(f"ERROR! : {e} :(")

if __name__ == "__main__":
    main()