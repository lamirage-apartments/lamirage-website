# Shrink phone photos for the website.
#   python3 resize-photos.py <folder of originals> <destination folder>
# Each .jpg/.jpeg/.png becomes a 1600px-long-side progressive JPEG at quality 82,
# with all metadata (including GPS location) dropped. Needs Pillow: pip3 install pillow

import sys, os
from PIL import Image, ImageOps

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)

for name in sorted(os.listdir(src)):
    base, ext = os.path.splitext(name)
    if ext.lower() not in (".jpg", ".jpeg", ".png"):
        continue
    im = Image.open(os.path.join(src, name))
    im = ImageOps.exif_transpose(im)           # honour the phone's rotation flag
    im = im.convert("RGB")
    im.thumbnail((1600, 1600), Image.LANCZOS)  # long side becomes 1600px, proportions kept
    out = os.path.join(dst, base + ".jpg")
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)  # no EXIF written
    print(f"{name} -> {out}  {im.size[0]}x{im.size[1]}  {os.path.getsize(out) // 1024} KB")
