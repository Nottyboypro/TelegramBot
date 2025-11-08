import asyncio
import importlib
from pyrogram import idle
from TelegramBot import LOGGER, app
from TelegramBotBot.core.dir import dirr
from TelegramBot.plugins import ALL_MODULES

async def init():
    # Ensure directories exist
    dirr()

    # Start the bot
    await app.start()
    LOGGER("TelegramBot").info("TelegramBot started successfully.")

    # Dynamically import plugins
    for module in ALL_MODULES:
        importlib.import_module("TelegramBot.plugins" + module)
    LOGGER("TelegramBot.plugins").info("Successfully Imported Modules...")

    # Keep the bot running
    await idle()

    # Stop the bot on exit
    await app.stop()
    LOGGER("TelegramBot").info("VoteBot stopped successfully.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
