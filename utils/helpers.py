# utils/helpers.py

import os
import shutil
from telegram import Update
from telegram.ext import CallbackContext
from config import FORCE_JOIN_CHANNEL
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def check_user_joined(update: Update, context: CallbackContext) -> bool:
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except:
        pass

    buttons = [[
        InlineKeyboardButton("✅ Subscribed", callback_data="make_pdf")
    ]]
    await update.callback_query.message.reply_text(
        f"🚫 You must join our channel to use this bot.\n\n👉 {FORCE_JOIN_CHANNEL}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return False

def clear_user_cache(user_id: int):
    folder = f"cache/{user_id}"
    pdf = f"cache/{user_id}.pdf"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    if os.path.exists(pdf):
        os.remove(pdf)

async def send_feature_buttons(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("📄 Make PDF", callback_data="make_pdf"),
            InlineKeyboardButton("📝 Set Name", callback_data="set_name")
        ],
        [
            InlineKeyboardButton("🧹 Clear", callback_data="clear"),
            InlineKeyboardButton("🌒 Dark Mode", callback_data="dark")
        ],
        [
            InlineKeyboardButton("💧 Your Watermark", callback_data="watermark"),
            InlineKeyboardButton("📦 Compress", callback_data="compress")
        ]
    ]
    await update.message.reply_text(
        "If you want to enable extra features, tap below. Otherwise, just tap 'Make PDF'.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
