from fastapi import APIRouter
import aiosqlite
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(__file__), "../../database/data.db")

@router.get("/leaderboard")
async def get_leaderboard():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT username, SUM(word_count) as total_words, COUNT(*) as total_messages
            FROM messages
            GROUP BY user_id
            ORDER BY total_words DESC
            LIMIT 10
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

@router.get("/top-words")
async def get_top_words():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT word, COUNT(*) as count
            FROM words
            GROUP BY word
            ORDER BY count DESC
            LIMIT 20
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

@router.get("/voice")
async def get_voice_leaderboard():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT username, SUM(duration_seconds) as total_seconds
            FROM voice_sessions
            WHERE duration_seconds IS NOT NULL
            GROUP BY user_id
            ORDER BY total_seconds DESC
            LIMIT 10
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]