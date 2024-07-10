import logging
from discord.ext import commands
from utils.utils import schedule_daily_message

def init_events(bot: commands.Bot, logger: logging.Logger) -> None:
    """Initialize events for the Discord bot"""
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user}")
        await schedule_daily_message(bot, logger)
