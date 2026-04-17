import sqlite3

conn = sqlite3.connect("sample.db")
conn.execute("DROP TABLE IF EXISTS customers")
conn.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        credit_card TEXT,
        phone TEXT
    )
""")
conn.executemany(
    "INSERT INTO customers (name, email, credit_card, phone) VALUES (?, ?, ?, ?)",
    [
        ("John Doe", "john.doe@gmail.com", "1234-5678-9012-3456", "6471234567"),
        ("Jane Smith", "jane.smith@yahoo.com", "9876-5432-1098-7654", "4161234567"),
        ("Bob Jones", "bob.jones@hotmail.com", "1111-2222-3333-4444", "9051234567"),
    ]
)
conn.commit()
conn.close()
print("sample.db created")