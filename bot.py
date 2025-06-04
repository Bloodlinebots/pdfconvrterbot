import os
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

from config import BOT_TOKEN
from pdf_generator import generate_pdf
from watermark import set_user_watermark, clear_user_watermark
from utils.helpers import clear_user_cache, send_feature_buttons, check_user_joined
from utils.filters import is_image

user_lang = {}
user_image_count = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_image_count.pop(user_id, None)

    keyboard = [
        [InlineKeyboardButton("English", callback_data=f"lang_en")]
    ]
    await update.message.reply_text(
        "Please choose your language:\n\nकृपया अपनी भाषा चुनें:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_lang[user_id] = query.data.split("_")[1]
    user_image_count.pop(user_id, None)

    await query.answer()
    await query.message.reply_text("Send your images (up to 20).")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    folder = Path(f"cache/{user_id}")
    folder.mkdir(parents=True, exist_ok=True)

    count = user_image_count.get(user_id, 0) + 1
    if count > 20:
        await update.message.reply_text("❌ You can send up to 20 images only.")
        return

    file_id = update.message.photo[-1].file_id if update.message.photo else update.message.document.file_id
    file = await context.bot.get_file(file_id)
    image_path = folder / f"{count}.jpg"
    await file.download_to_drive(str(image_path))

    user_image_count[user_id] = count
    await send_feature_buttons(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data == "make_pdf":
        joined = await check_user_joined(update, context)
        if not joined:
            return

        path = generate_pdf(user_id)
        with open(path, "rb") as pdf:
            await context.bot.send_document(
                chat_id=user_id,
                document=pdf,
                caption="Here is your PDF ✅"
            )
        clear_user_cache(user_id)
        user_image_count.pop(user_id, None)

    elif data == "set_name":
        await query.message.reply_text("Send me the name for the PDF file (not required yet). [Coming Soon]")
    elif data == "clear":
        clear_user_cache(user_id)
        user_image_count.pop(user_id, None)
        await query.message.reply_text("🧹 All images cleared.")
    elif data == "dark":
        await query.message.reply_text("🌒 Dark mode feature coming soon!")
    elif data == "watermark":
        await query.message.reply_text("Send your watermark text now:")
        context.user_data['expecting_watermark'] = True
    elif data == "compress":
        await query.message.reply_text("📦 Compress option will be enabled soon.")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.user_data.get('expecting_watermark'):
        wm = update.message.text.strip()
        set_user_watermark(user_id, wm)
        await update.message.reply_text("✅ Watermark set!")
        context.user_data['expecting_watermark'] = False

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Unknown command. Please use /start to begin.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(set_language, pattern="^lang_"))
    app.add_handler(MessageHandler(is_image, handle_image))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))  # fallback

    print("Bot running...")
    app.run_polling()
