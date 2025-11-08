from pyrogram.types import InlineKeyboardButton
import config
from TelegramBot import app


def start_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴛᴜᴛᴏʀɪᴀʟs", url="https://t.me/tgacselling/2"
            ),
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel():
    buttons = [
        [
            InlineKeyboardButton(text="ʜᴇʟᴘ ᴀɴᴅ ᴄᴀᴍᴍᴀɴᴅs", callback_data="settings_back_helper"),
        ],
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇs", url=config.SUPPORT_CHANNEL),
        ],
        [
            InlineKeyboardButton(
                text="ᴛᴜᴛᴏʀɪᴀʟs",
                url="https://t.me/tgacselling/2",
            )
        ],
        [
            InlineKeyboardButton(text="ʙᴏᴛ ᴏᴡɴᴇʀ", user_id=config.OWNER_ID),
        ],
    ]
    return buttons
