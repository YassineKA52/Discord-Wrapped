import discord
from discord.ext import commands
from datetime import datetime, timezone
from database.db import log_message, log_words, log_voice_join, log_voice_leave

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_join_times = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        words = [w for w in message.content.split() if w.isalpha()]
        word_count = len(words)
        timestamp = datetime.now(timezone.utc).isoformat()

        await log_message(
            user_id=str(message.author.id),
            username=str(message.author),
            channel_id=str(message.channel.id),
            word_count=word_count,
            timestamp=timestamp
        )

        if words:
            await log_words(
                user_id=str(message.author.id),
                username=str(message.author),
                words=words,
                timestamp=timestamp
            )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        # User joined a voice channel
        if before.channel is None and after.channel is not None:
            joined_at = datetime.now(timezone.utc).isoformat()
            self.voice_join_times[member.id] = joined_at
            await log_voice_join(
                user_id=str(member.id),
                username=str(member),
                channel_id=str(after.channel.id),
                joined_at=joined_at
            )

        # User left a voice channel
        elif before.channel is not None and after.channel is None:
            joined_at = self.voice_join_times.pop(member.id, None)
            if joined_at:
                left_at = datetime.now(timezone.utc).isoformat()
                from datetime import datetime as dt
                duration = int((dt.fromisoformat(left_at) - dt.fromisoformat(joined_at)).total_seconds())
                await log_voice_leave(
                    user_id=str(member.id),
                    joined_at=joined_at,
                    left_at=left_at,
                    duration_seconds=duration
                )

async def setup(bot):
    await bot.add_cog(Tracker(bot))