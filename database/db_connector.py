import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

    def get_tables(self) -> list[str]:
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        return [row[0] for row in cursor.fetchall()]

    def read_table(self, table: str) -> list[dict]:
        cursor = self.conn.execute(f"SELECT * FROM {table}")
        return [dict(row) for row in cursor.fetchall()]

    def write_table(self, table: str, records: list[dict]) -> None:
        if not records:
            return
        self.conn.execute(f"DROP TABLE IF EXISTS masked_{table}")
        columns = ", ".join(f"{k} TEXT" for k in records[0].keys())
        self.conn.execute(f"CREATE TABLE masked_{table} ({columns})")
        for record in records:
            placeholders = ", ".join("?" * len(record))
            self.conn.execute(
                f"INSERT INTO masked_{table} VALUES ({placeholders})",
                list(record.values())
            )
        self.conn.commit()

    def close(self):
        self.conn.close()