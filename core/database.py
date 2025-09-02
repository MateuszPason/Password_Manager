import sqlite3
import os

DB_PATH = "data/vault.db"


class DatabaseConnection:
    """Context manager for SQLite database connections."""
    def __enter__(self):
        self.conn = sqlite3.connect(DB_PATH)
        return self.conn
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

def get_connection():
    """Get a new database connection (legacy, prefer DatabaseConnection)."""
    return sqlite3.connect(DB_PATH)


def initialize_database() -> None:
    """
    Initialize the database and create required tables if they do not exist.
    """
    os.makedirs("data", exist_ok=True)
    with DatabaseConnection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password BLOB NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL
                )
            """)
            conn.commit()
        except Exception as e:
            raise e

def insert_credential(site: str, username: str, password: bytes) -> None:
    """
    Insert a new credential into the database.
    Args:
        site: The site name.
        username: The username.
        password: The encrypted password as bytes.
    """
    with DatabaseConnection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO credentials (site, username, password) VALUES (?, ?, ?)",
                (site, username, password)
            )
            conn.commit()
        except Exception as e:
            raise e

def search_credentials(query: str, cred_id: int = None) -> list[tuple]:
    """
    Search credentials by site/username or by credential ID.
    Args:
        query: The search string for site or username.
        cred_id: Optional credential ID for direct lookup.
    Returns:
        List of matching credential tuples.
    """
    with DatabaseConnection() as conn:
        try:
            cursor = conn.cursor()
            if cred_id is not None:
                cursor.execute("SELECT * FROM credentials WHERE id = ?", (cred_id,))
            else:
                cursor.execute(
                    "SELECT * FROM credentials WHERE site LIKE ? OR username LIKE ?",
                    (f"%{query}%", f"%{query}%")
                )
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            raise e

def insert_setting(key: str, value: str) -> None:
    """
    Insert or update a setting in the database.
    Args:
        key: The setting key.
        value: The setting value.
    """
    with DatabaseConnection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """, (key, value))
            conn.commit()
        except Exception as e:
            raise e

def get_setting(key: str) -> str | None:
    """
    Retrieve a setting value by key.
    Args:
        key: The setting key.
    Returns:
        The setting value if found, else None.
    """
    with DatabaseConnection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            raise e
    

def delete_credential(cred_id):
    """
    Delete a credential from the database by its ID.
    Args:
        cred_id: The credential ID to delete.
    """
    with DatabaseConnection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM credentials WHERE id=?", (cred_id,))
            conn.commit()
        except Exception as e:
            raise e
