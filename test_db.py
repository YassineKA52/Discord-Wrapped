import aiosqlite
import asyncio

async def check():
    async with aiosqlite.connect("database/data.db") as db:
        print("--- MESSAGES ---")
        async for row in await db.execute("SELECT * FROM messages"):
            print(row)

        print("\n--- TOP WORDS ---")
        async for row in await db.execute("""
            SELECT word, COUNT(*) as count 
            FROM words 
            GROUP BY word 
            ORDER BY count DESC 
            LIMIT 10
        """):
            print(row)

        print("\n--- VOICE SESSIONS ---")
        async for row in await db.execute("SELECT * FROM voice_sessions"):
            print(row)

asyncio.run(check())