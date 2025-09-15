import sqlite3
from datetime import datetime

DB_NAME = "sokoban_results.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm TEXT,
            speed TEXT,
            steps INTEGER,
            duration REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_result(algorithm, speed, steps, duration):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO game_results (algorithm, speed, steps, duration, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (algorithm, speed, steps, duration, timestamp))
    conn.commit()
    conn.close()
