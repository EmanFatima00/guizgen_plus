import sqlite3
from datetime import datetime

DB_NAME = "quiz_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    score INTEGER,
                    total INTEGER)''')
    conn.commit()
    conn.close()

def save_attempt(score, total):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO attempts (timestamp, score, total) VALUES (?, ?, ?)',
              (datetime.now().isoformat(), score, total))
    conn.commit()
    conn.close()

def get_history(limit=5):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT timestamp, score, total FROM attempts ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows