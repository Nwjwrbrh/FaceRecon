import sqlite3
import numpy as np

# 1. Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("college_club.db")
cursor = conn.cursor()

# 2. Create the 'club' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS club (
    Image BLOB NOT NULL
    RollNo INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL,
    embedding BLOB NOT NULL
""")
conn.commit()
print("Table 'club' created successfully.")

# --- Demonstration: How to Insert Data ---

# Simulate a 128-dimensional SFace embedding array (float32)
mock_embedding = np.random.randn(128).astype(np.float32)

# Convert the NumPy array to raw binary bytes for BLOB storage
embedding_bytes = mock_embedding.tobytes()

# Insert query data
student_data = (101, "Alice Smith", "Computer Science", embedding_bytes)



# --- Demonstration: How to Retrieve Data ---

cursor.execute("SELECT name, department, bin FROM club WHERE rollno = ?", (101,))
row = cursor.fetchone()

if row:
    retrieved_name, retrieved_dept, retrieved_bin = row
    
    # Reconstruct the NumPy array from the raw BLOB data
    # (SFace outputs float32, so we must specify the identical dtype)
    retrieved_embedding = np.frombuffer(retrieved_bin, dtype=np.float32)
    
    print("\n--- Retrieved Data ---")
    print(f"Name: {retrieved_name}")
    print(f"Dept: {retrieved_dept}")
    print(f"Embedding Shape: {retrieved_embedding.shape}")  # Should be (128,)
    print(f"First 3 values: {retrieved_embedding[:3]}")

# Close the database connection
conn.close()
