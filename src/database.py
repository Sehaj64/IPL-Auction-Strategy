import sqlite3
import os

# Define the path to the database file relative to this script's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_FILE = os.path.join(BASE_DIR, 'database', 'ipl_auction.db')


def get_db_connection():
    """Establishes a connection to the database."""
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database by first deleting the old one, then creating
    the schema.
    """
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

    conn = get_db_connection()
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.close()
    print("Database schema initialized.")


def load_sample_data():
    """Loads sample player data into the database from data.sql."""
    conn = get_db_connection()
    data_path = os.path.join(BASE_DIR, 'database', 'data.sql')
    with open(data_path, 'r') as f:
        conn.executescript(f.read())
    conn.close()
    print("Sample player data loaded.")


if __name__ == '__main__':
    init_db()
    load_sample_data()
