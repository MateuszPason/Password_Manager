import sqlite3
import os

DB_PATH = "data/vault.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            password BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()
