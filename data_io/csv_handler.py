import csv

def read_csv(path: str) -> list[dict]:
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def write_csv(path: str, records: list[dict]) -> None:
    if not records:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)