from fastapi import APIRouter
import aiosqlite
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(__file__), "../../database/data.db")

@router.get("/monthly")
async def get_monthly_recap():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        # Top messenger
        cursor = await db.execute("""
            SELECT username, SUM(word_count) as total_words, COUNT(*) as total_messages
            FROM messages
            GROUP BY user_id
            ORDER BY total_messages DESC
            LIMIT 1
        """)
        top_messenger = dict(await cursor.fetchone() or {})

        # Most used word
        cursor = await db.execute("""
            SELECT word, COUNT(*) as count
            FROM words
            GROUP BY word
            ORDER BY count DESC
            LIMIT 1
        """)
        top_word = dict(await cursor.fetchone() or {})

        # Most time in voice
        cursor = await db.execute("""
            SELECT username, SUM(duration_seconds) as total_seconds
            FROM voice_sessions
            WHERE duration_seconds IS NOT NULL
            GROUP BY user_id
            ORDER BY total_seconds DESC
            LIMIT 1
        """)
        top_voice = dict(await cursor.fetchone() or {})

        return {
            "top_messenger": top_messenger,
            "top_word": top_word,
            "top_voice": top_voice
        }