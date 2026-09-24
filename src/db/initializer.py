import sqlite3
import sqlite_vec


def dbInitializer(path : str):
    db = sqlite3.connect(path)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)

    db.execute("PRAGMA foreign_keys = ON")
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        Image BLOB NOT NULL,
        RollNo INTEGER NOT NULL,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        Position TEXT NOT NULL,
        "Joined On" DATE DEFAULT (date('now'))
    );
    """)

    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS FaceVectors USING vec0(
        embedding float[128]
    );
    """)

    db.commit()
    db.close()
    print("Table 'Users , FaceVectors' created successfully.")

    
