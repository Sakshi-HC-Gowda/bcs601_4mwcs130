import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    amount   REAL,
    category TEXT,
    date     TEXT
)
""")

conn.commit()
conn.close()
print("Database created successfully!")
