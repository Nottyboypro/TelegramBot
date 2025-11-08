import re
from pyrogram import filters

# ==========================
# 🔧 Configuration (Direct Values)
# ==========================

# Telegram API Credentials (from https://my.telegram.org/apps)
API_ID = 24168862
API_HASH = "916a9424dd1e58ab7955001ccc0172b3"

# Bot Token (from @BotFather)
BOT_TOKEN = "8376342482:AAFZfOIkjgTYyvcNYzxkjoIjKQBUzGOMqsE"

# MongoDB Connection URL (from https://cloud.mongodb.com)
MONGO_DB_URI = "mongodb+srv://jaydipmore74:xCpTm5OPAfRKYnif@cluster0.5jo18.mongodb.net/?retryWrites=true&w=majority"

# Log group/chat ID
LOGGER_ID = -1002023049910

# Heroku (optional)
HEROKU_APP_NAME = "xxxx"
HEROKU_API_KEY = "herokuapikeyexample1234567890"

# Owner and admin Telegram ID
OWNER_ID = 6421770811, 

# Upstream Repo Config
UPSTREAM_REPO = "https://github.com/Nottyboypro/VoteBot"
UPSTREAM_BRANCH = "main"

# If private repo, Git Token
GIT_TOKEN = "xxxx"

# Support Links
SUPPORT_CHANNEL = "https://t.me/ZeeMusicUpdate"
SUPPORT_CHAT = "https://t.me/ZeeMusicSupport"
SUPPORT_GROUP = "https://t.me/ZeeMusicSupport"

# ==========================
# 📸 Image URLs
# ==========================

START_IMG_URL = "https://files.catbox.moe/6nzevm.jpg"
STATS_IMG_URL = "https://graph.org/file/99a8a9c13bb01f9ac7d98.png"
PING_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"



# ==========================
# 🔒 URL Validation
# ==========================

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )
