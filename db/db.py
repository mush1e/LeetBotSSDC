import sqlite3
from config import env

def init_db() -> None:
    """Initialize sqlite3 database and creates users table"""
    conn = sqlite3.connect(env.DATABASE_FILE)

    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_id TEXT UNIQUE,
        username TEXT,
        streak INTEGER DEFAULT 0,
        solved INTEGER DEFAULT 0,
        last_solved DATE
    )''')

    conn.commit()
    conn.close()
