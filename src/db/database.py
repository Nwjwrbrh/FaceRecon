import sqlite3
import sqlite_vec

def init(dbName : str) -> None :
    """To init the database schema"""

    db = sqlite3.connect("database.db")
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
        created_at DATE DEFAULT (date('now'))
    );
    """)

    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS FaceVectors USING vec0(
        embedding float[128]
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        day_no INTEGER NOT NULL,
        attendance_date DATE NOT NULL,

        FOREIGN KEY (user_id)
            REFERENCES Users(id)
            ON DELETE CASCADE,

        UNIQUE (user_id, attendance_date)
    );
    """)

    db.commit()
    print("Table 'Users , FaceVectors , Attendence' created successfully.")
    db.close()


def connectDB(dbName : str) -> None :
    pass
