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
    async def register(ctx):
        """Registers a user"""
        user_id = ctx.author.id
        username = str(ctx.author)
        db_name = f'{ctx.guild.id}_leetbot.db'
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (discord_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()
            await ctx.send(f"{username} has been registered.")
        except sqlite3.IntegrityError:
            await ctx.send("You are already registered.")
        conn.close()

    # Command: !solved
    @bot.command()
    async def solved(ctx):
        """Marks the daily problem as solved"""
        user_id = ctx.author.id
        today = datetime.date.today()
        db_name = f'{ctx.guild.id}_leetbot.db'
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT last_solved, streak FROM users WHERE discord_id = ?", (user_id,))
        result = c.fetchone()
        if result:
            last_solved, streak = result
            if last_solved is None or datetime.datetime.strptime(last_solved, "%Y-%m-%d").date() < today:
                new_streak = streak + 1 if last_solved is None or datetime.datetime.strptime(last_solved, "%Y-%m-%d").date() == today - datetime.timedelta(days=1) else 1
                c.execute("UPDATE users SET last_solved = ?, streak = ?, solved = solved + 1 WHERE discord_id = ?", (today, new_streak, user_id))
                conn.commit()
                await ctx.send(f"{ctx.author} has solved today's problem! Streak: {new_streak} days.")
            else:
                await ctx.send("You have already solved today's problem.")
        else:
            await ctx.send("You need to register first using `/register`.")
        conn.close()

    # Command: !leaderboard
    @bot.command()
    async def leaderboard(ctx):
        """Displays the leaderboard"""
        db_name = f'{ctx.guild.id}_leetbot.db'
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT username, solved FROM users ORDER BY solved DESC LIMIT 10")
        leaderboard = c.fetchall()
        conn.close()
        if leaderboard:
            message = "🏆 **Leaderboard** 🏆\n\n"
            for i, (username, solved) in enumerate(leaderboard, start=1):
                message += f"{i}. {username}: {solved} problems solved\n"
            await ctx.send(message)
        else:
            await ctx.send("No one has solved any problems yet.")