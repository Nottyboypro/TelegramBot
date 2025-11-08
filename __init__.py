from TelegramBot.core.bot import Bot
from TelegramBot.core.dir import dirr
from TelegramBot.misc import dbb, heroku

from .logging import LOGGER

dirr()
dbb()
heroku()

app = Bot()
