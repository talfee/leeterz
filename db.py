import sqlite3
from contextlib import contextmanager

DB_PATH = 'database.db'

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS friends (
                user_id INTEGER NOT NULL,
                friend_id INTEGER NOT NULL,
                UNIQUE(user_id, friend_id)
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS stats (
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                count INTEGER NOT NULL,
                titles TEXT,
                PRIMARY KEY(user_id, date)
            )"""
        )
        conn.commit()
