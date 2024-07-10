
import discord
from discord.ext import commands

def init_bot() -> commands.Bot:
  """Initialize Discord bot with specific configuration"""
  intents = discord.Intents.default()
  intents.message_content = True

  return commands.Bot(command_prefix='!', intents=intents)
