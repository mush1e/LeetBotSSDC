import settings
import requests
import datetime
import asyncio
import sqlite3
import discord
from discord.ext import commands

# ~~~~~~~~~~~~~~~~~~~~~~~ Set Up Logger and DB ~~~~~~~~~~~~~~~~~~~~~~~
logger = settings.logging.getLogger("bot")
DATABASE = 'leetbot.db'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Initialize DB ~~~~~~~~~~~~~~~~~~~~~~~~~~~
def init_db():
    """Initialize SQLite database if not exists."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_id TEXT UNIQUE,
        username TEXT,
        streak INTEGER DEFAULT 0,
        solved INTEGER DEFAULT 0,
        last_solved DATE
    )''')
    conn.commit()
    conn.close()

# ~~~~~~~~~~~~~~~~~~~~~~ Fetch Problem of the Day ~~~~~~~~~~~~~~~~~~~~~
def fetch_daily_problem():
    """Fetches the daily problem from an external API."""
    url = 'https://alfa-leetcode-api.onrender.com//daily'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Driver Method ~~~~~~~~~~~~~~~~~~~~~~~~~~~
def run():
    """Runs the bot with Discord API integration."""
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # ~~~~~~~~~~~~~~~~~~~~~~~ Event Handler: on_ready ~~~~~~~~~~~~~~~~~~~~~~~~
    # Event triggered when the bot has successfully connected to Discord.
    # Logs the user information and schedules the daily problem posting.
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user}")
        await schedule_daily_message()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~ Command: !daily ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Command that posts the daily LeetCode problem to the channel.
    @bot.command()
    async def daily(ctx):
        """Posts Daily Question"""
        problem_data = fetch_daily_problem()
        if problem_data:
            problem_title = problem_data['questionTitle']
            problem_link = problem_data['questionLink']
            message = f"# Today's LeetCode Daily Problem:\n\n**{problem_title}**\n{problem_link}\n\nGood Luck! (Don't post your solutions without a spoiler!)"
        else:
            message = "# Error procuring todays problem\nTry again later :("
        await ctx.send(message)

    # ~~~~~~~~~~~~~~~~~~~~~~~ Command: !register ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Command that registers a user in the SQLite database.
    @bot.command()
    async def register(ctx):
        """Registers a user"""
        user_id = ctx.author.id
        username = str(ctx.author)
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (discord_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()
            await ctx.send(f"{username} has been registered.")
        except sqlite3.IntegrityError:
            await ctx.send("You are already registered.")
        conn.close()

    # ~~~~~~~~~~~~~~~~~~~~~~~ Command: !solved ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Command that marks the daily problem as solved for a user.
    @bot.command()
    async def solved(ctx):
        """Marks the daily problem as solved"""
        user_id = ctx.author.id
        today = datetime.date.today()
        conn = sqlite3.connect(DATABASE)
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

    # ~~~~~~~~~~~~~~~~~~~~~~~ Command: !leaderboard ~~~~~~~~~~~~~~~~~~~~~~~~
    # Command that displays the leaderboard based on solved problems.
    @bot.command()
    async def leaderboard(ctx):
        """Displays the leaderboard"""
        conn = sqlite3.connect(DATABASE)
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

    # ~~~~~~~~~~~~~~~~~~~~ Helper Function: post_daily_problem ~~~~~~~~~~~~~~~~~
    # Posts the daily problem to the specified channel.
    async def post_daily_problem(channel):
        problem_data = fetch_daily_problem()
        if problem_data:
            problem_title = problem_data['questionTitle']
            problem_link = problem_data['questionLink']
            message = f"# Today's LeetCode Daily Problem:\n\n**{problem_title}**\n{problem_link}\n\nGood Luck! (Don't post your solutions without a spoiler!)"
        else:
            message = "# Error procuring today's problem\nTry again later :("
        await channel.send(message)

    # ~~~~~~~~~~~~~~~~~~~~ Helper Function: schedule_daily_message ~~~~~~~~~~~~~
    # Continuously schedules the daily problem posting based on current time.
    async def schedule_daily_message():
        while True:
            now = datetime.datetime.now()
            then = now.replace(hour=0, minute=0, second=0, microsecond=0)
            if now >= then:
                then += datetime.timedelta(days=1)
            wait_time = (then - now).total_seconds()
            logger.info(f"Waiting for {wait_time} seconds until next post.")
            await asyncio.sleep(wait_time)
            channel = bot.get_channel(settings.CHANNEL_ID)
            if channel:
                await post_daily_problem(channel)
            else:
                logger.error("Channel not found. Ensure the CHANNEL_ID is correct.")

    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    init_db()
    run()
