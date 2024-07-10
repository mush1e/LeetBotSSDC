import datetime
import sqlite3
from config import env
from discord.ext import commands
from utils.utils import post_daily_problem, create_embed

def init_commands(bot: commands.Bot) -> None:
    """Initialize commands for the Discord bot"""
    # Command: !daily
    @bot.command()
    async def daily(ctx: commands.Context) -> None:
        """Posts Daily Question"""
        channel = bot.get_channel(env.CHANNEL_ID)
        await post_daily_problem(channel)

    # Command: !register
    @bot.command()
    async def register(ctx: commands.Context) -> None:
        """Registers a user"""
        user_id = ctx.author.id
        username = str(ctx.author)
        conn = sqlite3.connect(env.DATABASE_FILE)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (discord_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()
            await ctx.send(embed=create_embed(title="Successfully registered!", link=None, description=f"{username} has been registered.", fields=None, color=0x6dd539))
        except sqlite3.IntegrityError:
            await ctx.send(embed=create_embed(title="An error has occurred!", link=None, description="You are already registered.", fields=None, color=0xd64340))
        conn.close()

    # Command: !solved
    @bot.command()
    async def solved(ctx: commands.Context) -> None:
        """Marks the daily problem as solved"""
        user_id = ctx.author.id
        today = datetime.date.today()
        conn = sqlite3.connect(env.DATABASE_FILE)
        c = conn.cursor()
        c.execute("SELECT last_solved, streak FROM users WHERE discord_id = ?", (user_id,))
        result = c.fetchone()
        if result:
            last_solved, streak = result
            if last_solved is None or datetime.datetime.strptime(last_solved, "%Y-%m-%d").date() < today:
                new_streak = streak + 1 if last_solved is None or datetime.datetime.strptime(last_solved, "%Y-%m-%d").date() == today - datetime.timedelta(days=1) else 1
                c.execute("UPDATE users SET last_solved = ?, streak = ?, solved = solved + 1 WHERE discord_id = ?", (today, new_streak, user_id))
                conn.commit()
                await ctx.send(embed=create_embed(title="Horray!", link=None, description=f"{ctx.author} has solved today's problem! Streak: {new_streak} days.", fields=None, color=0x6dd539))
            else:
                await ctx.send(embed=create_embed(title="An error has occurred!", link=None, description="You have already solved today's problem.", fields=None, color=0xd64340))
        else:
            await ctx.send(embed=create_embed(title="Not registered", link=None, description="You need to register first using `/register`.", fields=None, color=0xd57b38))
        conn.close()

    # Command: !leaderboard
    @bot.command()
    async def leaderboard(ctx: commands.Context) -> None:
        """Displays the leaderboard"""
        conn = sqlite3.connect(env.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT username, solved FROM users ORDER BY solved DESC LIMIT 10")
        leaderboard = cursor.fetchall()
        conn.close()
        if leaderboard:
            message = "🏆 **Leaderboard** 🏆\n\n"
            for i, (username, solved) in enumerate(leaderboard, start=1):
                message += f"{i}. {username}: {solved} problems solved\n"
            await ctx.send(embed=create_embed(title="Leaderboard", link=None, description=message, fields=None, color=0x6dd539))
        else:
            await ctx.send(embed=create_embed(title="No leaderboard available", link=None, description="No one has solved any problems yet.", fields=None, color=0xd57b38))
