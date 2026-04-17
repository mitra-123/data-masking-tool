import json

def read_json(path: str) -> list[dict]:
    with open(path, "r") as f:
        return json.load(f)

def write_json(path: str, records: list[dict]) -> None:
    with open(path, "w") as f:
        json.dump(records, f, indent=2)