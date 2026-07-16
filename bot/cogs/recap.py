import discord
from discord.ext import commands
import aiosqlite
import os
from anthropic import Anthropic

DB_PATH = os.path.join(os.path.dirname(__file__), "../../database/data.db")
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class Recap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leaderboard(self, ctx):
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row

            # Top messagers
            cursor = await db.execute("""
                SELECT username, SUM(word_count) as total_words, COUNT(*) as total_messages
                FROM messages
                GROUP BY user_id
                ORDER BY total_messages DESC
                LIMIT 5
            """)
            top_messages = await cursor.fetchall()

            # Top words
            cursor = await db.execute("""
                SELECT word, COUNT(*) as count
                FROM words
                GROUP BY word
                ORDER BY count DESC
                LIMIT 5
            """)
            top_words = await cursor.fetchall()

            # Top voice
            cursor = await db.execute("""
                SELECT username, SUM(duration_seconds) as total_seconds
                FROM voice_sessions
                WHERE duration_seconds IS NOT NULL
                GROUP BY user_id
                ORDER BY total_seconds DESC
                LIMIT 5
            """)
            top_voice = await cursor.fetchall()

        embed = discord.Embed(
            title="📊 Server Leaderboard",
            color=discord.Color.blurple()
        )

        # Messages leaderboard
        if top_messages:
            value = "\n".join([
                f"`{i+1}.` **{row['username']}** — {row['total_messages']} messages ({row['total_words']} words)"
                for i, row in enumerate(top_messages)
            ])
        else:
            value = "No data yet!"
        embed.add_field(name="💬 Most Messages", value=value, inline=False)

        # Top words
        if top_words:
            value = "\n".join([
                f"`{i+1}.` **{row['word']}** — {row['count']} times"
                for i, row in enumerate(top_words)
            ])
        else:
            value = "No data yet!"
        embed.add_field(name="🔤 Most Used Words", value=value, inline=False)

        # Voice leaderboard
        if top_voice:
            value = "\n".join([
                f"`{i+1}.` **{row['username']}** — {round(row['total_seconds'] / 60, 1)} minutes"
                for i, row in enumerate(top_voice)
            ])
        else:
            value = "No voice data yet!"
        embed.add_field(name="🎙️ Most Time in Voice", value=value, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def recap(self, ctx):
        async with ctx.typing():
            async with aiosqlite.connect(DB_PATH) as db:
                db.row_factory = aiosqlite.Row

                cursor = await db.execute("""
                    SELECT username, SUM(word_count) as total_words, COUNT(*) as total_messages
                    FROM messages
                    GROUP BY user_id
                    ORDER BY total_messages DESC
                    LIMIT 5
                """)
                top_messages = await cursor.fetchall()

                cursor = await db.execute("""
                    SELECT word, COUNT(*) as count
                    FROM words
                    GROUP BY word
                    ORDER BY count DESC
                    LIMIT 5
                """)
                top_words = await cursor.fetchall()

                cursor = await db.execute("""
                    SELECT username, SUM(duration_seconds) as total_seconds
                    FROM voice_sessions
                    WHERE duration_seconds IS NOT NULL
                    GROUP BY user_id
                    ORDER BY total_seconds DESC
                    LIMIT 5
                """)
                top_voice = await cursor.fetchall()

            if not top_messages and not top_voice:
                await ctx.send("Pas assez de données pour générer un récap encore !")
                return

            stats_summary = (
                f"Top messagers: {[(r['username'], r['total_messages']) for r in top_messages]}\n"
                f"Top words: {[(r['word'], r['count']) for r in top_words]}\n"
                f"Top voice time (seconds): {[(r['username'], r['total_seconds']) for r in top_voice]}"
            )

            message = claude_client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": (
                        "Voici les statistiques d'activité d'un serveur Discord ce mois-ci. "
                        "Écris un résumé fun et court (5-6 phrases max) façon 'Spotify Wrapped', "
                        "en français, qui met en valeur les membres les plus actifs.\n\n"
                        f"{stats_summary}"
                    )
                }]
            )
            summary_text = message.content[0].text

        embed = discord.Embed(
            title="✨ Récap Mensuel — généré par IA",
            description=summary_text,
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Recap(bot))