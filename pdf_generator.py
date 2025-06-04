# pdf_generator.py

from PIL import Image
from watermark import apply_watermarks
from pathlib import Path
import os

def resize_img(img):
    max_size = (1240, 1754)  # A4 size at 150 DPI
    img.thumbnail(max_size, Image.ANTIALIAS)
    return img

def generate_pdf(user_id):
    folder = Path(f"cache/{user_id}")
    images = []

    for file_name in sorted(os.listdir(folder), key=lambda x: int(x.split('.')[0])):
        path = folder / file_name
        img = Image.open(path).convert("RGB")
        img = resize_img(img)

        # Add watermark and footer here
        img = apply_watermarks(img, user_id)
        images.append(img)

    output_path = f"cache/{user_id}.pdf"
    if images:
        images[0].save(output_path, save_all=True, append_images=images[1:])
    return output_path
