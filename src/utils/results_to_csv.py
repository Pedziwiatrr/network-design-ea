import json
import csv
import os
import argparse


def json_to_csv(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found.")
        return

    with open(input_path, "r") as f:
        data = json.load(f)

    if not data:
        print("Error: JSON file is empty.")
        return

    columns = [
        "mode",
        "modularity",
        "best_cost",
        "mean_cost",
        "std_cost",
        "avg_convergence",
        "avg_time",
    ]

    try:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns, delimiter=";")

            headers = {col: col.replace("_", " ").upper() for col in columns}
            writer.writerow(headers)

            for row in data:
                clean_row = {col: row.get(col) for col in columns}

                for key, val in clean_row.items():
                    if isinstance(val, float):
                        clean_row[key] = str(val).replace(".", ",")

                writer.writerow(clean_row)

        print(f"Success! :) Saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="results/results.json")
    parser.add_argument("--output_file", type=str, default="results/results_excel.csv")
    args = parser.parse_args()

    json_to_csv(args.input_file, args.output_file)
