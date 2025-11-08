import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pyrogram.enums import ChatMemberStatus, ChatType

from TelegramBot import app, LOGGER
from TelegramBot.utils.database import add_served_user, get_served_users, is_served_user
from TelegramBot.utils.inline.start import private_panel  # <-- added
import config

# Tiny bold text converter
def tiny(text: str) -> str:
    table = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    )
    return f"{text.translate(table)}"

START_IMAGES = [
    "https://files.catbox.moe/x5lytj.jpg",
    "https://files.catbox.moe/psya34.jpg",
    "https://files.catbox.moe/leaexg.jpg"
]

@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    user = message.from_user
    try:
        await add_served_user(user.id)
    except:
        pass

    # Animated welcome
    try:
        msg = await message.reply_text(tiny(f"ʜᴇʏ {user.first_name} 👋"))
        await asyncio.sleep(0.7)
        await msg.edit_text(tiny("ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ Telegram ᴀᴄᴄᴏᴜɴᴛ Sell ʙᴏᴛ"))
        await asyncio.sleep(0.7)
        await msg.edit_text(tiny("ʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ᴅᴀsʜʙᴏᴀʀᴅ..."))
        await asyncio.sleep(0.7)
        await msg.delete()
    except:
        pass

    caption = tiny(
        "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀᴄᴄᴏᴜɴᴛ ʙᴏᴛ - ꜰᴀsᴛᴇsᴛ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ sᴇʟʟᴇʀ ʙᴏᴛ\n\n"
        "• ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴏᴛᴘs 🔧\n"
        "• ᴇᴀsʏ ᴛᴏ ᴜsᴇ 🙌\n"
        "• 24/7 sᴜᴘᴘᴏʀᴛ 👨‍💻\n"
        "• ɪɴsᴛᴀɴᴛ ᴘᴀʏᴍᴇɴᴛ ᴀᴘᴘʀᴏᴠᴀʟs 🧾\n\n"
        "🚀 ʜᴏᴡ ᴛᴏ ᴜsᴇ:\n"
        "1️⃣ ʀᴇᴄʜᴀʀɢᴇ\n"
        "2️⃣ sᴇʟᴇᴄᴛ ᴄᴏᴜɴᴛʀʏ\n"
        "3️⃣ ʙᴜʏ ᴀᴄᴄᴏᴜɴᴛ / ɢᴇᴛ ɴᴜᴍʙᴇʀ\n"
        "4️⃣ ʟᴏɢɪɴ ᴛʜʀᴏᴜɢʜ ᴛᴇʟᴇɢʀᴀᴍ ᴏʀ ᴛᴇʟᴇɢʀᴀᴍ 𝕏\n"
        "5️⃣ ʀᴇᴄᴇɪᴠᴇ ᴏᴛᴘ & ʏᴏᴜ’ʀᴇ ᴅᴏɴᴇ ✅\n\n"
        "ᴇɴᴊᴏʏ ꜰᴀsᴛ ᴀᴄᴄᴏᴜɴᴛ ʙᴜʏɪɴɢ ᴇxᴘᴇʀɪᴇɴᴄᴇ 🎉"
    )

    # Load buttons from private_panel instead of hardcoding
    out = private_panel() # if your private_panel expects language dict, pass None
    reply_markup = InlineKeyboardMarkup(out)

    await message.reply_photo(
        photo=random.choice(START_IMAGES),
        caption=caption,
        reply_markup=reply_markup
    )
