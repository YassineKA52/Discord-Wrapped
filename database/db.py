import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                word_count INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                word TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS voice_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                joined_at TEXT NOT NULL,
                left_at TEXT,
                duration_seconds INTEGER
            )
        """)
        await db.commit()

async def log_message(user_id, username, channel_id, word_count, timestamp):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO messages (user_id, username, channel_id, word_count, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, channel_id, word_count, timestamp))
        await db.commit()

async def log_words(user_id, username, words, timestamp):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany("""
            INSERT INTO words (user_id, username, word, timestamp)
            VALUES (?, ?, ?, ?)
        """, [(user_id, username, word.lower(), timestamp) for word in words])
        await db.commit()

async def log_voice_join(user_id, username, channel_id, joined_at):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO voice_sessions (user_id, username, channel_id, joined_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, channel_id, joined_at))
        await db.commit()

async def log_voice_leave(user_id, joined_at, left_at, duration_seconds):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE voice_sessions
            SET left_at = ?, duration_seconds = ?
            WHERE user_id = ? AND joined_at = ?
        """, (left_at, duration_seconds, user_id, joined_at))
        await db.commit()