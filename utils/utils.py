import re
import datetime
import asyncio
import logging
import discord
from config import env
from typing import NoReturn
from discord.ext import commands
from discord.abc import GuildChannel, PrivateChannel
from api.api import fetch_daily_problem

remove_html = re.compile('<[^>]*>|&([a-z0-9]+|#[\d]{1,6}|#x[0-9a-f]{1,6});')

def create_embed(title: str, link: str | None, description: str | None, fields: list[tuple[str, str, bool]] | None, color: int) -> discord.Embed:
    """Create an embed to send with a given message"""
    embed=discord.Embed(title=title, url=link, description=description, color=color)

    embed.set_author(name=env.EMBED_NAME, url=env.EMBED_URL, icon_url=env.EMBED_ICON_URL)
    embed.set_thumbnail(url=env.EMBED_THUMBNAIL_URL)

    if fields:
        for field, value, inline in fields:
            embed.add_field(name=field, value=value, inline=inline)

    return embed

async def post_daily_problem(channel: GuildChannel | PrivateChannel | discord.Thread | None) -> None:
    """Posts the daily problem to the specified channel."""
    problem_data = fetch_daily_problem()
    if problem_data:
        problem_title = problem_data['questionTitle']
        problem_link = problem_data['questionLink']
        problem_description = problem_data['question']
        problem_difficulty = problem_data["difficulty"]
        problem_likes = problem_data["likes"]
        problem_dislikes = problem_data["dislikes"]
        processed_description = re.sub(remove_html, '', problem_description)
        processed_description = processed_description.replace('\n', '')

        await channel.send(embed=create_embed(title=problem_title, link=problem_link, description=f"```{processed_description}```", fields=
                                              [("Difficulty", problem_difficulty, True), ("Likes", problem_likes, True), ("Dislikes", problem_dislikes, True)], color=0xd4af37))
    else:
        await channel.send(embed=create_embed(title="Oops! An error occurred", link=None, description="# Error procuring today's problem\nTry again later :(", fields=None, color=0xd64340))

async def schedule_daily_message(bot: commands.Bot, logger: logging.Logger) -> NoReturn:
    """Continuously schedules the daily problem posting based on current time."""
    while True:
        now = datetime.datetime.now()
        then = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if now >= then:
            then += datetime.timedelta(days=1)
        wait_time = (then - now).total_seconds()
        logger.info(f"Waiting for {wait_time} seconds until next post.")
        await asyncio.sleep(1000)
        for guild in bot.guilds:
            channel = bot.get_channel(env.CHANNEL_ID) 
            if channel:
                await post_daily_problem(channel)
            else:
                logger.error(f"Channel not found for guild {guild.name} (ID: {guild.id}). Ensure the CHANNEL_ID is correct.")
