from config import env
from db.db import init_db
from config.bot import init_bot
from config.logging import logger
from events.events import init_events
from commands.commands import init_commands

def run() -> None:
    bot = init_bot()

    init_events(bot, logger)
    init_commands(bot)

    bot.run(env.BOT_TOKEN, root_logger=True)

if __name__ == "__main__":
    init_db()
    run()
