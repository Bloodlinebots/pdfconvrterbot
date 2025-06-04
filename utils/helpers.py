# utils/helpers.py

import os
import shutil
from telegram import Update
from telegram.ext import CallbackContext
from config import FORCE_JOIN_CHANNEL

async def check_user_joined(update: Update, context: CallbackContext) -> bool:
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except:
        pass

    buttons = [[
        context.bot.inline_keyboard_button("✅ Subscribed", callback_data="make_pdf")
    ]]
    await update.callback_query.message.reply_text(
        "🚫 You must join our channel to use this bot.\n\n👉 @image_to_pdf",
        reply_markup=context.bot.inline_keyboard_markup(buttons)
    )
    return False

def clear_user_cache(user_id: int):
    folder = f"cache/{user_id}"
    pdf = f"cache/{user_id}.pdf"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    if os.path.exists(pdf):
        os.remove(pdf)

def send_feature_buttons(update: Update, context: CallbackContext):
    buttons = [
        [
            context.bot.inline_keyboard_button("📄 Make PDF", callback_data="make_pdf"),
            context.bot.inline_keyboard_button("📝 Set Name", callback_data="set_name")
        ],
        [
            context.bot.inline_keyboard_button("🧹 Clear", callback_data="clear"),
            context.bot.inline_keyboard_button("🌒 Dark Mode", callback_data="dark")
        ],
        [
            context.bot.inline_keyboard_button("💧 Your Watermark", callback_data="watermark"),
            context.bot.inline_keyboard_button("📦 Compress", callback_data="compress")
        ]
    ]
    update.message.reply_text(
        "If you want to enable extra features, tap below. Otherwise, just tap 'Make PDF'.",
        reply_markup=context.bot.inline_keyboard_markup(buttons)
    )
  
