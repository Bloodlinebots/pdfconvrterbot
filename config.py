# config.py

import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
FORCE_JOIN_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL", "@image_to_pdf")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "123456789"))

# You can use dotenv or set these in deployment env
