# filters.py

from telegram import Message
from telegram.ext import filters

def is_image_filter(message: Message) -> bool:
    if message.photo:
        return True
    if message.document and message.document.mime_type:
        return message.document.mime_type.startswith("image/")
    return False
