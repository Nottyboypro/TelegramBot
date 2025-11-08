from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from TelegramBot import app
from TelegramBot.utils.inline.help import help_back_markup, help_pannel, private_help_panel
from config import START_IMG_URL, SUPPORT_CHAT

# ⬇️ NEW: bring the shim + long help texts from your helpers
from strings.helpers import get_string, DEFAULT_LANG
from strings import helpers


# Default language (change if you want a different default)
DEFAULT_LANG = "en"

# HELP command for private and callback
@app.on_message(filters.command(["help"]) & filters.private)
@app.on_callback_query(filters.regex("settings_back_helper"))
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        # Direct message instead of get_string
        caption = f"✨ ʜᴇʟᴘ ᴍᴇɴᴜ ✨\n\n ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ \n\n sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ:{SUPPORT_CHAT}"
        keyboard = help_pannel(True)
        await update.edit_message_text(caption, reply_markup=keyboard)
    else:
        try:
            await update.delete()
        except:
            pass
        caption = f"✨ ʜᴇʟᴘ ᴍᴇɴᴜ \n\nᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ .\n\n sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ: {SUPPORT_CHAT}"
        keyboard = help_pannel()
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=caption,
            reply_markup=keyboard,
        )


# HELP command for groups
@app.on_message(filters.command(["help"]) & filters.group)
async def help_com_group(client, message: Message):
    text = (
        "📮 **Use the button below to open help in PM.**\n\n"
        "You can view all available commands and their categories there."
    )
    keyboard = private_help_panel()
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# HELP callback for help sections
@app.on_callback_query(filters.regex("help_callback"))
async def helper_cb(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup()

    # Directly show help sections from helpers
    if cb == "hb1":
        await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)
    elif cb == "hb5":
        await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)
    elif cb == "hb6":
        await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)
    elif cb == "hb7":
        await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
    elif cb == "hb8":
        await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)
    elif cb == "hb9":
        await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
    elif cb == "hb10":
        await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)
    elif cb == "hb11":
        await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)
    elif cb == "hb12":
        await CallbackQuery.edit_message_text(helpers.HELP_12, reply_markup=keyboard)
    elif cb == "hb13":
        await CallbackQuery.edit_message_text(helpers.HELP_13, reply_markup=keyboard)
    elif cb == "hb14":
        await CallbackQuery.edit_message_text(helpers.HELP_14, reply_markup=keyboard)
    elif cb == "hb15":
        await CallbackQuery.edit_message_text(helpers.HELP_15, reply_markup=keyboard)
