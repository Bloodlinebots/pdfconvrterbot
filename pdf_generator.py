from PIL import Image
from watermark import apply_watermarks
from pathlib import Path
import os

def resize_img(img):
    max_size = (1240, 1754)  # A4 size approx
    img.thumbnail(max_size)
    return img

def generate_pdf(user_id):
    folder = Path(f"cache/{user_id}")
    images = []

    for file_name in sorted(os.listdir(folder), key=lambda x: int(x.split('.')[0])):
        path = folder / file_name
        img = Image.open(path).convert("RGB")
        img = resize_img(img)
        img = apply_watermarks(img, user_id)
        images.append(img)

    output_path = folder.parent / f"{user_id}.pdf"  # cache/{user_id}.pdf
    if images:
        images[0].save(output_path, save_all=True, append_images=images[1:])
    return str(output_path)
