import aiosqlite
import asyncio

async def check():
    async with aiosqlite.connect("database/data.db") as db:
        async for row in await db.execute("SELECT * FROM messages"):
            print(row)

asyncio.run(check())