import sqlite3
import os

def get_db_connection(db_path=None):
    if db_path is None:
        db_path = os.getenv("DB_PATH", "output/asana_simulation.sqlite")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(schema_path="schema.sql", db_path=None):
    conn = get_db_connection(db_path)
    try:
        with open(schema_path, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()
