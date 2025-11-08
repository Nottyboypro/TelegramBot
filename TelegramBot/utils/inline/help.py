from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TelegramBot import app


def help_pannel(START: Union[bool, int] = None):
    # Footer row depends on START (same logic as before)
    first = [InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")]
    second = [
        InlineKeyboardButton(
            text="ʙᴀᴄᴋ",
            callback_data="settingsback_helper",  # kept as-is from your snippet
        ),
    ]
    mark = second if START else first

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="💰 ʙᴀʟᴀɴᴄᴇ", callback_data="help_callback hb1"),
                InlineKeyboardButton(text="🛒 ʙᴜʏ ᴀᴄᴄᴏᴜɴᴛ", callback_data="help_callback hb2"),
                InlineKeyboardButton(text="💳 ʀᴇᴄʜᴀʀɢᴇ", callback_data="help_callback hb3"),
            ],
            [
                InlineKeyboardButton(text="🎁 ʀᴇᴅᴇᴇᴍ", callback_data="help_callback hb4"),
                InlineKeyboardButton(text="🥂 ʀᴇꜰᴇʀ & ᴇᴀʀɴ", callback_data="help_callback hb5"),
                InlineKeyboardButton(text="ᴘʀᴏғɪʟᴇ", callback_data="help_callback hb6"),
            ],
            [
                InlineKeyboardButton(text="ᴛᴏᴘ- sᴇʟʟɪɴɢ", callback_data="help_callback hb7"),
                InlineKeyboardButton(text="ᴘʀɪᴍɪᴜᴍ ᴀᴄᴄᴏᴜɴᴛ", callback_data="help_callback hb8"),
                InlineKeyboardButton(text="sᴛᴏʀʏ ғᴇᴀᴛᴜʀᴇ", callback_data="help_callback hb9"),
            ],
            [
                InlineKeyboardButton(text="ʀᴇᴄʜᴀʀɢᴇ sᴛᴀᴛᴜs", callback_data="help_callback hb10"),
                InlineKeyboardButton(text="ʙᴜʟᴋ ʙᴜʏ", callback_data="help_callback hb11"),
                InlineKeyboardButton(text="ᴍʏ ʀᴇғᴇʀᴀʟs", callback_data="help_callback hb12"),
            ],
            [
                InlineKeyboardButton(text="ᴅɪsᴄᴏᴜɴᴛ", callback_data="help_callback hb13"),
                InlineKeyboardButton(text="ʜᴇɪɢʜ ᴘʀɪᴄᴇ ᴀᴄ", callback_data="help_callback hb14"),
                InlineKeyboardButton(text="ʟᴏᴡ ᴘʀɪᴄᴇ ᴀᴄ", callback_data="help_callback hb15"),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ʙᴀᴄᴋ",
                    callback_data="settings_back_helper",  # kept as-is from your snippet
                ),
            ]
        ]
    )


def private_help_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="Open Help",
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
