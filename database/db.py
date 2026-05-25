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
        await db.commit()

async def log_message(user_id, username, channel_id, word_count, timestamp):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO messages (user_id, username, channel_id, word_count, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, channel_id, word_count, timestamp))
        await db.commit()