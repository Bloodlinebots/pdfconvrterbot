# watermark.py

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

FOOTER_TEXT = "Made with @pdf_maker_rbot"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Change path if needed
FONT_SIZE = 24

# Optional: Store user watermark if needed (dictionary or persistent method)
user_watermarks = {}

def apply_watermarks(image: Image.Image, user_id: int) -> Image.Image:
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Draw user's watermark if exists
    user_text = user_watermarks.get(user_id)
    if user_text:
        draw.text((width // 2, 40), user_text, font=font, fill=(0, 0, 0), anchor="ms")

    # Draw footer at bottom
    draw.text((width // 2, height - 40), FOOTER_TEXT, font=font, fill=(100, 100, 100), anchor="ms")

    return image

def set_user_watermark(user_id: int, text: str):
    user_watermarks[user_id] = text

def clear_user_watermark(user_id: int):
    if user_id in user_watermarks:
        del user_watermarks[user_id]
      
