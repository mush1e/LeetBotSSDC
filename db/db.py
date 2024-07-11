import sqlite3

def init_db(guild_id) -> None:
    """Initialize SQLite database for the specified guild if not exists."""
    db_name = f'{guild_id}_leetbot.db'
    conn = sqlite3.connect(db_name)
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
