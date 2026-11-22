import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "college_chatbot.db"
DATA_PATH = BASE_DIR / "dataset" / "college_data.json"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_seed_data():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def init_db():
    data = load_seed_data()
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS college_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS qa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'bot')),
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        for key, value in data.get("college", {}).items():
            conn.execute(
                "INSERT INTO college_info(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, str(value))
            )
        # Seed Q&A only when table is empty; edits to JSON can be loaded by resetting DB.
        count = conn.execute("SELECT COUNT(*) FROM qa").fetchone()[0]
        if count == 0:
            for intent in data.get("intents", []):
                for question in intent.get("patterns", []):
                    for answer in intent.get("responses", []):
                        conn.execute(
                            "INSERT INTO qa(tag, question, answer) VALUES(?, ?, ?)",
                            (intent["tag"], question, answer)
                        )
        conn.commit()

def get_qa_rows():
    with get_connection() as conn:
        return [dict(row) for row in conn.execute(
            "SELECT id, tag, question, answer FROM qa ORDER BY id"
        ).fetchall()]

def get_college_info():
    with get_connection() as conn:
        return {row["key"]: row["value"] for row in conn.execute(
            "SELECT key, value FROM college_info"
        ).fetchall()}

def save_message(session_id, role, message):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO chat_history(session_id, role, message) VALUES(?, ?, ?)",
            (session_id, role, message)
        )
        conn.commit()

def get_history(session_id, limit=100):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT role, message, created_at FROM chat_history "
            "WHERE session_id=? ORDER BY id DESC LIMIT ?",
            (session_id, limit)
        ).fetchall()
    return [dict(row) for row in reversed(rows)]

def clear_history(session_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM chat_history WHERE session_id=?", (session_id,))
        conn.commit()
