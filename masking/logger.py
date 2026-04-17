from dataclasses import dataclass, field
from typing import defaultdict

@dataclass
class MaskingReport:
    total_records: int = 0
    masked_fields: dict = field(default_factory=lambda: defaultdict(int))

    def record_mask(self, field_name: str):
        self.masked_fields[field_name] += 1

    def increment_records(self):
        self.total_records += 1

    def print_summary(self):
        print("\n===== Masking Report =====")
        print(f"Total records processed: {self.total_records}")
        print("Fields masked:")
        for field_name, count in self.masked_fields.items():
            print(f"  - {field_name}: {count} values masked")
        print("==========================\n")