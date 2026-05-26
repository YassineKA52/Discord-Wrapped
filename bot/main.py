import discord
from discord.ext import commands
from dotenv import load_dotenv
from database.db import init_db
import asyncio
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await init_db()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"📡 Connected to {len(bot.guilds)} server(s)")
    print("📝 Message tracker active")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

async def main():
    async with bot:
        await bot.load_extension("bot.cogs.tracker")
        await bot.load_extension("bot.cogs.recap")
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())