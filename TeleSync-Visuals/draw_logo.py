#!/usr/bin/env python3
"""TeleSync logo: a single boundary stone, a squat gritstone post with its top
dished into a shallow hollow, flat silhouette in sea grey, the hollow shadowed
in iron dark, one amber fleck where low sun catches the wet dip. Beneath,
TeleSync in Anton SC, tight and upright in iron. At 64px, stone and hollow
only: the dipped top is the whole signature."""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W = H = 1024
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
GREY = (116, 122, 124); GREY_D = (92, 98, 100); IRON = (44, 46, 48); AMBER = (232, 164, 62)
img = Image.new("RGB", (W, H), (226, 224, 216)); d = ImageDraw.Draw(img, "RGBA")
x0, y0, x1, y1 = 292, 170, 732, 640
d.polygon([(x0 + 18, y0 + 60), (x1 - 18, y0 + 60), (x1 - 44, y1), (x0 + 44, y1)], fill=GREY)
d.polygon([(x0, y0), (x1, y0), (x1 - 18, y0 + 62), (x0 + 18, y0 + 62)], fill=(134, 140, 142))
# the dished hollow
hw = 120 if v == "v1" else 168
d.ellipse([512 - hw, y0 + 8, 512 + hw, y0 + 58], fill=IRON)
d.ellipse([512 - hw + 22, y0 + 16, 512 + hw - 22, y0 + 50], fill=(96, 92, 78))
d.ellipse([512 - 52, y0 + 22, 512 + 30, y0 + 40], fill=(206, 168, 96))  # water in the dip
d.ellipse([512 - 18, y0 + 25, 512 + 2, y0 + 35], fill=AMBER)  # one amber fleck of low sun
rng = np.random.default_rng(7)
for _ in range(160):  # grit
    gx = rng.integers(x0 + 40, x1 - 40); gy = rng.integers(y0 + 84, y1 - 12)
    d.ellipse([gx, gy, gx + 5, gy + 4], fill=GREY_D)
d.rectangle([x0 + 30, y1 - 26, x1 - 30, y1 - 14], fill=(84, 88, 90))  # ground shadow line
if v != "v1":
    f = ImageFont.truetype("fonts/AntonSC.ttf", 104)
    txt = "TeleSync"; tw = d.textlength(txt, font=f)
    d.text(((W - tw) / 2, 712), txt, font=f, fill=IRON)
a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "logo.png" if v == "ship" else f"scratch/logo-{v}.png"
img.save(out); print(out)
img.resize((64, 64), Image.LANCZOS).save(f"scratch/logo64-{v}.png"); print("64px saved")
