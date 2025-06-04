from PIL import Image, ImageDraw, ImageFont

FOOTER_TEXT = "Made with @pdf_maker_rbot"
FONT_SIZE = 20

user_watermarks = {}

def apply_watermarks(image: Image.Image, user_id: int) -> Image.Image:
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font = ImageFont.load_default()

    # Draw user's watermark (top center)
    user_text = user_watermarks.get(user_id)
    if user_text:
        draw.text((width / 2, 30), user_text, font=font, fill="black", anchor="ms")

    # Draw footer (bottom center)
    draw.text((width / 2, height - 30), FOOTER_TEXT, font=font, fill="gray", anchor="ms")

    return image

def set_user_watermark(user_id: int, text: str):
    user_watermarks[user_id] = text

def clear_user_watermark(user_id: int):
    user_watermarks.pop(user_id, None)
