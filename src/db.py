import sqlite3

def get_connection(db_path='sales.db'):
    """Create and return database connection"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def close_connection(conn):
    """Close database connection"""
    if conn:
        conn.close()