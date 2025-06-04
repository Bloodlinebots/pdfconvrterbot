# filters.py

from telegram.ext import MessageFilter

class IsImage(MessageFilter):
    def filter(self, message):
        return message.photo or (message.document and message.document.mime_type.startswith("image/"))

is_image = IsImage()
