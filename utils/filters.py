# filters.py

from telegram.ext import MessageFilter

class IsImage(MessageFilter):
    def filter(self, message) -> bool:
        if message.photo:
            return True
        if message.document and message.document.mime_type:
            return message.document.mime_type.startswith("image/")
        return False

is_image = IsImage()
