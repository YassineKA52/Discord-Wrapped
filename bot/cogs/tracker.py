import discord
from discord.ext import commands
from datetime import datetime, timezone
from database.db import log_message

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        word_count = len(message.content.split())
        timestamp = datetime.now(timezone.utc).isoformat()

        await log_message(
            user_id=str(message.author.id),
            username=str(message.author),
            channel_id=str(message.channel.id),
            word_count=word_count,
            timestamp=timestamp
        )

async def setup(bot):
    await bot.add_cog(Tracker(bot))