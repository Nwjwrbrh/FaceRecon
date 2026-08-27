import sqlite3

conn = sqlite3.connect("records.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS club (
    Image BLOB NOT NULL,
    RollNo INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL,
    embedding BLOB NOT NULL,
    Status TEXT NOT NULL,
    Timestamp TEXT NOT NULL 
    )
""")
conn.commit()
print("Table 'club' created successfully.")

conn.close()
