\
import sqlite3
import os

DATABASE_DIR = "data"
DATABASE_PATH = os.path.join(DATABASE_DIR, "soundfresh.db")

def ensure_db_directory():
    """Ensures the database directory exists."""
    os.makedirs(DATABASE_DIR, exist_ok=True)

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    ensure_db_directory()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
    return conn

def initialize_database():
    """Initializes the database and creates tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            name TEXT,
            last_name TEXT,
            age INTEGER,
            gender TEXT,
            country TEXT,
            email TEXT UNIQUE,
            registration_date TEXT NOT NULL
        )
    ''')

    # Create playlists table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name_playlist TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    # Create playlist_songs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlist_songs (
            playlist_song_id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_id INTEGER,
            song_path TEXT NOT NULL,
            FOREIGN KEY(playlist_id) REFERENCES playlists(playlist_id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")

if __name__ == '__main__':
    initialize_database()
