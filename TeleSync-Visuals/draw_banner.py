#!/usr/bin/env python3
"""TeleSync wordmark banner: dusk along the lane leaving Eyam, stretched wide
and nearly empty of people. Midground: the boundary stone at the lane edge,
hollow full of rainwater reflecting the last light, a small sack and a loaf on
the grass a respectful distance on the village side, an empty handcart further
off on the outside with handles lowered. Cottages with doors shut, one window
lit amber, one chimney smoking. TeleSync is cut into a flat gritstone slab by
the church gate at left, Anton SC forms weathered pale against dark stone."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W, H = 2560, 640
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
GREY = (116, 122, 124); IRON = (44, 46, 48); AMBER = (232, 164, 62); OAK = (110, 82, 52)
img = Image.new("RGB", (W, H), (104, 112, 116)); d = ImageDraw.Draw(img, "RGBA")
for x in range(W):
    t = x / W
    d.line([(x, 0), (x, 300)], fill=(int(140 - 34 * t), int(144 - 32 * t), int(144 - 28 * t)))
d.polygon([(0, 330), (700, 262), (1500, 282), (2560, 300), (2560, 380), (0, 380)], fill=(96, 84, 64))  # moor
# church tower silhouette behind the slab, left of centre
d.rectangle([700, 90, 790, 330], fill=(56, 56, 54)); d.rectangle([692, 72, 798, 92], fill=(46, 46, 44))
d.rectangle([728, 150, 762, 220], fill=(28, 28, 28))
# cottages near side, doors shut, one window lit
for cx, cw in ((1560, 430), (2060, 460)):
    d.rectangle([cx, 220, cx + cw, 380], fill=(120, 110, 96))
    d.polygon([(cx - 16, 220), (cx + cw + 16, 220), (cx + cw // 2, 156)], fill=(64, 54, 42))
    d.rectangle([cx + 60, 288, cx + 118, 380], fill=OAK)
    lit = (cx == 1560)
    d.rectangle([cx + 220, 262, cx + 282, 316], fill=AMBER if lit else (50, 52, 52))
    d.rectangle([cx + 330, 262, cx + 392, 316], fill=(50, 52, 52))
d.rectangle([2240, 128, 2272, 190], fill=(98, 90, 78))
smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(smoke)
for i in range(7):
    sx = 2256 + i * 22; sy = 118 - i * 24; r = 13 + i * 8
    sd.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2], fill=(198, 200, 198, 44))
img = Image.alpha_composite(img.convert("RGBA"), smoke.filter(ImageFilter.GaussianBlur(10))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# ground and lane running past the stone, unguarded beyond it
d.rectangle([0, 380, W, H], fill=(84, 90, 60))
d.polygon([(880, 640), (1330, 420), (1560, 392), (1900, 392), (1620, 640)], fill=(116, 110, 98))
# the slab by the church gate at left, carrying the cut name
d.polygon([(90, 470), (640, 452), (668, 560), (110, 586)], fill=(74, 76, 78))
d.polygon([(90, 470), (640, 452), (668, 560), (110, 586)], outline=(52, 54, 56), width=5)
f = ImageFont.truetype("fonts/AntonSC.ttf", 96 if v == "ship" else 62)
txt = "TeleSync"; tw = d.textlength(txt, font=f)
d.text((90 + (578 - tw) / 2, 478), txt, font=f, fill=(214, 210, 196))
# boundary stone midground at the lane edge, hollow full of rainwater
sx, sy = 1408, 418
d.polygon([(sx, sy + 18), (sx + 104, sy + 18), (sx + 94, sy + 108), (sx + 10, sy + 108)], fill=GREY)
d.polygon([(sx - 5, sy), (sx + 109, sy), (sx + 104, sy + 20), (sx, sy + 20)], fill=(134, 140, 142))
d.ellipse([sx + 14, sy + 2, sx + 90, sy + 17], fill=(216, 180, 106))
for cxx in (sx + 34, sx + 58):
    d.ellipse([cxx, sy + 7, cxx + 10, sy + 12], fill=(242, 200, 96))
# sack and loaf on the grass, village side, a respectful distance off
d.polygon([(1180, 500), (1248, 500), (1236, 452), (1192, 452)], fill=(168, 146, 104))
d.ellipse([1276, 486, 1332, 504], fill=(196, 158, 96))
# empty handcart beyond the stone, handles lowered, owner gone
hx, hy = 1830, 430
d.rectangle([hx, hy, hx + 190, hy + 52], fill=OAK)
for lx in (hx + 18, hx + 160):
    d.rectangle([lx, hy + 52, lx + 12, hy + 96], fill=(84, 62, 38))
d.ellipse([hx + 66, hy + 62, hx + 124, hy + 120], outline=(40, 38, 34), width=8)
d.line([(hx + 190, hy + 40), (hx + 262, hy + 92)], fill=OAK, width=10)
d.line([(hx + 190, hy + 10), (hx + 258, hy + 60)], fill=OAK, width=10)
rng = np.random.default_rng(9); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "banner.png" if v == "ship" else f"scratch/banner-{v}.png"
img.save(out); print(out)
