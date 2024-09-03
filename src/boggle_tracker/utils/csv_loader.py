import csv
from typing import List, Dict


def load_csv(file_path: str) -> List[Dict]:
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            holdings = list(reader)
            if not holdings:
                print(f"Warning: CSV file {file_path} is empty or has no valid data.")
            return holdings
    except FileNotFoundError:
        print(f"Warning: CSV file not found: {file_path}")
        return []
    except csv.Error as e:
        print(f"Warning: Error reading CSV file {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error reading CSV file {file_path}: {e}")
        return []
