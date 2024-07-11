import logging
from discord.ext import commands
from utils.utils import schedule_daily_message
from db.db import init_db

def init_events(bot: commands.Bot, logger: logging.Logger) -> None:
    """Initialize events for the Discord bot"""
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user}")
        await schedule_daily_message(bot, logger)
        
        # Initialize DB for all existing guilds
        for guild in bot.guilds:
            init_db(guild.id)
            logger.info(f"Initialized DB for guild: {guild.name} with ID: {guild.id}")

    @bot.event
    async def on_guild_join(guild):
        init_db(guild.id)
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
