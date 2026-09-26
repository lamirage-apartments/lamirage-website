# Shrink phone photos for the website.
#   python3 resize-photos.py <folder of originals> <destination folder>
# Each .jpg/.jpeg/.png becomes a 1600px-long-side progressive JPEG at quality 82,
# with all metadata (including GPS location) dropped. Needs Pillow: pip3 install pillow

import sys, os, io
from PIL import Image, ImageOps, ImageCms

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
SRGB = ImageCms.createProfile("sRGB")

for name in sorted(os.listdir(src)):
    base, ext = os.path.splitext(name)
    if ext.lower() not in (".jpg", ".jpeg", ".png"):
        continue
    im = Image.open(os.path.join(src, name))
    icc = im.info.get("icc_profile")
    im = ImageOps.exif_transpose(im)           # honour the phone's rotation flag
    im = im.convert("RGB")
    if icc:
        # Convert to standard web colour before the profile is dropped, otherwise photos
        # saved in Display P3 (iPhones) or ProPhoto come out dull or with shifted colours.
        try:
            im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode="RGB")
        except Exception:
            print(f"  note: could not read the colour profile in {name}; colours kept as they are")
    im.thumbnail((1600, 1600), Image.LANCZOS)  # long side becomes 1600px, proportions kept
    out = os.path.join(dst, base + ".jpg")
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)  # no EXIF, no colour profile
    print(f"{name} -> {out}  {im.size[0]}x{im.size[1]}  {os.path.getsize(out) // 1024} KB")
