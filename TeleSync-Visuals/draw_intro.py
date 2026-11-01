#!/usr/bin/env python3
"""TeleSync intro banner: Eyam's edge at dusk, no lettering or emblem of any kind.
Foreground: rough grass and a worn path ending abruptly at the boundary stone,
its vinegar hollow brimming, coins glinting under the water, a dropped length
of string trailing toward the village. Midground: the lane bending past shut
cottages, a well with its bucket on the rim, bare washing lines. Background:
the church tower in dark gritstone against a sea grey sky, the moor behind
the rooftops, crows settling on a dead tree, the road beyond the stone empty
to the horizon. The brimming hollow with coins under water is the memory."""
import sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
W, H = 1600, 900
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
GREY = (128, 138, 142); IRON = (44, 46, 48); AMBER = (232, 164, 62); OAK = (110, 82, 52)
img = Image.new("RGB", (W, H), (106, 116, 120)); d = ImageDraw.Draw(img, "RGBA")
# sea grey sky lightening at the failing west (left)
for x in range(W):
    t = x / W
    d.line([(x, 0), (x, 430)], fill=(int(148 - 42 * t), int(150 - 36 * t), int(148 - 32 * t)))
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
ld.polygon([(0, 120), (430, 200), (300, 430), (0, 430)], fill=(255, 186, 96, 52 if v == "v1" else 76))
img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(26))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# moor rising behind the rooftops
d.polygon([(0, 430), (360, 330), (820, 356), (1240, 316), (1600, 366), (1600, 470), (0, 470)], fill=(94, 80, 62))
d.polygon([(0, 430), (360, 330), (820, 356), (900, 400), (300, 440)], fill=(104, 90, 68))
# church tower in dark gritstone
tx = 1050
d.rectangle([tx, 190, tx + 120, 430], fill=(58, 58, 56))
d.rectangle([tx - 10, 168, tx + 130, 192], fill=(48, 48, 46))
for px in (tx + 18, tx + 82):
    d.rectangle([px, 140, px + 10, 170], fill=(48, 48, 46))
d.rectangle([tx + 42, 250, tx + 78, 316], fill=(30, 30, 30))
d.rectangle([tx + 50, 258, tx + 70, 308], fill=(70, 66, 58))
# dead tree at the parish edge with crows settling
d.line([(1330, 430), (1318, 300)], fill=(40, 36, 32), width=12)
for bx, by, bl in ((1318, 300, -70), (1322, 330, 74), (1320, 268, 52)):
    d.line([(1320, by + 30), (1320 + bl, by)], fill=(40, 36, 32), width=6)
for cxx, cyy in ((1258, 288), (1388, 318), (1368, 252)):
    d.ellipse([cxx, cyy, cxx + 26, cyy + 13], fill=(22, 22, 24))
    d.ellipse([cxx + 20, cyy - 7, cxx + 32, cyy + 3], fill=(22, 22, 24))
# shut cottages along the lane, one window lit amber, one chimney smoking
for i, (cx, cw, ch) in enumerate(((90, 300, 150), (430, 260, 132), (730, 230, 118))):
    cy = 430 - ch
    d.rectangle([cx, cy, cx + cw, 430], fill=(122, 112, 98))
    d.polygon([(cx - 14, cy), (cx + cw + 14, cy), (cx + cw // 2, cy - 62)], fill=(66, 56, 44))
    d.rectangle([cx + 34, 352, cx + 82, 430], fill=OAK)
    for wx in (cx + 130, cx + 196):
        lit = (i == 1 and wx == cx + 130)
        d.rectangle([wx, 330, wx + 44, 378], fill=AMBER if lit else (52, 54, 54))
        d.line([(wx, 354), (wx + 44, 354)], fill=(40, 38, 34), width=3)
    if i == 0:
        d.rectangle([cx + 210, cy - 96, cx + 238, cy - 40], fill=(100, 92, 80))
smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(smoke)
for i in range(8):
    sx = 334 + i * 17; sy = 240 - i * 30; r = 15 + i * 8
    sd.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2], fill=(196, 198, 196, 46))
img = Image.alpha_composite(img.convert("RGBA"), smoke.filter(ImageFilter.GaussianBlur(11))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# bare washing lines between two houses
d.line([(390, 336), (430, 330)], fill=(210, 208, 200), width=3); d.line([(390, 352), (430, 346)], fill=(210, 208, 200), width=2)
# the lane bending through, and the ground: rough grass foreground
d.polygon([(0, 900), (0, 430), (1600, 430), (1600, 900)], fill=(86, 92, 62))
d.polygon([(520, 900), (760, 560), (900, 470), (1060, 452), (1240, 452), (1080, 560), (1020, 900)], fill=(118, 112, 100))
# well with bucket resting on the rim, nobody drawing water
d.rectangle([180, 470, 300, 540], fill=(104, 100, 92)); d.rectangle([168, 458, 312, 476], fill=(84, 80, 72))
d.rectangle([196, 428, 216, 460], fill=(70, 58, 40)); d.rectangle([264, 428, 284, 460], fill=(70, 58, 40))
d.line([(206, 434), (274, 434)], fill=(70, 58, 40), width=5)
d.polygon([(236, 448), (272, 448), (264, 486), (244, 486)], fill=(96, 74, 46))
# worn path ending abruptly at the stone
d.polygon([(560, 900), (700, 700), (742, 610), (806, 610), (790, 700), (830, 900)], fill=(138, 128, 108))
# THE boundary stone, foreground centre right: squat gritstone post, dished top
sx, sy, sw, sh = 786, 548, 196, 216
d.polygon([(sx, sy + 30), (sx + sw, sy + 30), (sx + sw - 14, sy + sh), (sx + 14, sy + sh)], fill=(112, 116, 118))
d.polygon([(sx - 8, sy), (sx + sw + 8, sy), (sx + sw, sy + 34), (sx, sy + 34)], fill=(132, 136, 138))
d.ellipse([sx + 18, sy + 2, sx + sw - 18, sy + 30], fill=(52, 56, 58))  # the hollow, shadowed
water_a = 150 if v == "v1" else 205
d.ellipse([sx + 26, sy + 6, sx + sw - 26, sy + 26], fill=(214, 178, 104, water_a))  # brimming water holding the sky
rng = np.random.default_rng(12)
for _ in range(90):  # grit speckle in the stone body
    gx = rng.integers(sx + 12, sx + sw - 12); gy = rng.integers(sy + 44, sy + sh - 8)
    d.ellipse([gx, gy, gx + 4, gy + 3], fill=(88, 92, 94))
for cxx, cyy in ((822, 566), (866, 571), (908, 564)):  # coins glinting under the water
    d.ellipse([cxx, cyy, cxx + 15, cyy + 6], fill=(240, 198, 96, 220))
# dropped string trailing from the stone toward the village
pts = [(700, 742), (648, 766), (604, 752), (556, 786), (508, 780)]
d.line(pts, fill=(206, 196, 168), width=4)
# grass heads along the bottom edge
rng = np.random.default_rng(12)
for _ in range(120):
    gx = rng.integers(0, W); gh = rng.integers(18, 64)
    d.line([(gx, 900), (gx + rng.integers(-9, 9), 900 - gh)], fill=(66, 74, 48), width=3)
a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "intro-banner.png" if v == "ship" else f"scratch/intro-{v}.png"
img.save(out); print(out)
