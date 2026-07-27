#!/usr/bin/env python3
"""
Rebuild avatar-idle-v2.gif from the approved native sprite.

Inputs (same directory):
  step2_final_opt5.png   approved 69x220 native sprite, RGBA, option-5 skin
  masks.npy              4 boolean layer masks: head, torso, arm, legs
  layout.json            canvas + bubble geometry
  GeistPixel-Regular-VariableFont_ELSH.ttf

Output:
  avatar-idle-vN.gif     bump N, never overwrite (GitHub camo caches)

Requires: pillow, numpy
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "avatar-idle-v3.gif"
# Integer upscale, NEAREST only. Browsers smooth-scale a stretched GIF and
# GitHub strips image-rendering:pixelated, so size has to be baked in native.
SCALE = int(sys.argv[2]) if len(sys.argv) > 2 else 1
HERE = os.path.dirname(os.path.abspath(__file__))
p = lambda f: os.path.join(HERE, f)

# ---------------------------------------------------------------- constants
BG       = (13, 17, 23)     # #0D1117  GitHub dark canvas
TEXT_C   = (230, 237, 243)  # #E6EDF3  GitHub default text
BORDER   = (139, 148, 158)  # #8B949E  muted, so text stays brightest
SKIN_MID = (145, 105, 69)   # blink fill (option-5 midtone)

FONT_SIZE   = 11
CHAR_MS     = 70    # per typed character
BOB_EVERY   = 7     # frames per bob step -> ~490ms
HOLD_FRAMES = 10
HOLD_MS     = 500
BLINK_MS    = 120
BLINK_AT    = 5     # index within hold phase
PALETTE_N   = 32

BOB = [0, -1, 0, 1]   # torso vertical offset
ARM = [0,  0, -1, 0]  # arm vertical offset
# head uses BOB[i-1] -- the one-frame lag is what sells it as alive

NECK_ROW   = 44
EYE_ROW    = 24
LENS_SPANS = [(21, 28), (33, 40)]

# ---------------------------------------------------------------- load
L = json.load(open(p("layout.json")))
lines  = L["lines"]
LH, PAD = L["LH"], L["PAD"]
BUB_X, BUB_Y = L["BUB_X"], L["BUB_Y"]
bub_w, bub_h = L["bub_w"], L["bub_h"]
CHAR_X, CHAR_Y = L["CHAR_X"], L["CHAR_Y"]
W, H = L["W"], L["H"]

font = ImageFont.truetype(p("GeistPixel-Regular-VariableFont_ELSH.ttf"), FONT_SIZE)

src   = np.array(Image.open(p("step2_final_opt5.png")).convert("RGBA"), dtype=np.uint8)
masks = np.load(p("masks.npy"))   # head, torso, arm, legs

def layer(m):
    o = np.zeros_like(src)
    o[m] = src[m]
    return Image.fromarray(o, "RGBA")

head, torso, arm, legs = (layer(m) for m in masks)

# blink variant C: eye row -> skin midtone, inside lens spans only
alpha = src[:, :, 3]
hb = np.array(head, dtype=np.int32)
for x0, x1 in LENS_SPANS:
    for x in range(x0, x1 + 1):
        if alpha[EYE_ROW, x] > 128 and src[EYE_ROW, x, :3].astype(int).sum() < 260:
            hb[EYE_ROW, x, :3] = SKIN_MID
head_blink = Image.fromarray(hb.astype(np.uint8), "RGBA")

# ---------------------------------------------------------------- draw
def draw_bubble(d):
    d.rectangle([BUB_X, BUB_Y, BUB_X + bub_w, BUB_Y + bub_h],
                fill=BG, outline=BORDER, width=1)
    ty = BUB_Y + 20
    for i in range(1, 8):                      # stepped tail, hand-plotted
        x = BUB_X - i
        d.point((x, ty - (7 - i)), fill=BORDER)
        d.point((x, ty + (7 - i)), fill=BORDER)
        if 7 - i > 0:
            d.line([(x, ty - (7 - i) + 1), (x, ty + (7 - i) - 1)], fill=BG)
    d.line([(BUB_X, ty - 7), (BUB_X, ty + 7)], fill=BG)

def build(bob_i, nchars, cursor, blink):
    c = Image.new("RGB", (W, H), BG)
    b   = BOB[bob_i % 4]
    a   = ARM[bob_i % 4]
    hbo = BOB[(bob_i - 1) % 4]                 # head lags one frame

    c.paste(legs,  (CHAR_X, CHAR_Y),       legs)
    c.paste(torso, (CHAR_X, CHAR_Y + b),   torso)
    c.paste(arm,   (CHAR_X, CHAR_Y + a),   arm)
    hd = head_blink if blink else head
    c.paste(hd,    (CHAR_X, CHAR_Y + hbo), hd)

    if hbo < b:                                # patch the neck gap
        patch = np.zeros((1, src.shape[1], 4), np.uint8)
        patch[0] = src[NECK_ROW]
        pi = Image.fromarray(patch, "RGBA")
        c.paste(pi, (CHAR_X, CHAR_Y + NECK_ROW + b - 1), pi)

    d = ImageDraw.Draw(c)
    draw_bubble(d)

    rem = nchars
    for i, ln in enumerate(lines):
        if rem <= 0:
            break
        show = ln[:rem]
        d.text((BUB_X + PAD, BUB_Y + PAD + i * LH), show, font=font, fill=TEXT_C)
        if cursor and rem <= len(ln):
            cx = BUB_X + PAD + int(font.getlength(show))
            d.rectangle([cx, BUB_Y + PAD + i * LH + 2,
                         cx + 5, BUB_Y + PAD + i * LH + 11], fill=TEXT_C)
            cursor = False
        rem -= len(ln)
    return c

# ---------------------------------------------------------------- sequence
total = sum(len(l) for l in lines)
frames, durs, fi = [], [], 0

for n in range(1, total + 1):                  # typing
    frames.append(build(fi // BOB_EVERY, n, True, False))
    durs.append(CHAR_MS); fi += 1

for k in range(HOLD_FRAMES):                   # hold + cursor blink + eye blink
    bl = (k == BLINK_AT)
    frames.append(build(fi // BOB_EVERY, total, k % 2 == 0, bl))
    durs.append(BLINK_MS if bl else HOLD_MS); fi += 1

# ---------------------------------------------------------------- scale
# NEAREST NEIGHBOR only -- smooth resampling turns a 1px outline into a 2px
# grey smear. Integer factors only, so every source pixel maps to an exact
# SxS block and no new colors are introduced.
OW, OH = W * SCALE, H * SCALE
if SCALE != 1:
    frames = [f.resize((OW, OH), Image.NEAREST) for f in frames]

# ---------------------------------------------------------------- quantize
# ONE global palette across every frame. Quantizing frames independently
# gives each its own color table and frames 2+ render as garbage.
merged = Image.new("RGB", (OW, OH * len(frames)))
for i, f in enumerate(frames):
    merged.paste(f, (0, i * OH))
master = merged.quantize(colors=PALETTE_N, method=Image.MEDIANCUT)
q = [f.quantize(palette=master, dither=Image.NONE) for f in frames]

q[0].save(p(OUT), save_all=True, append_images=q[1:],
          duration=durs, loop=0, disposal=2, optimize=True)

# ---------------------------------------------------------------- verify
g = Image.open(p(OUT))
allc = set()
for i in range(g.n_frames):
    g.seek(i)
    allc |= set(map(tuple, np.unique(np.array(g.convert("RGB")).reshape(-1, 3), axis=0)))

ok = True
for name, (y, x) in {"jeans": (170, 40), "bg": (2, 2), "shoe": (215, 30)}.items():
    y, x = y * SCALE, x * SCALE      # probes are native coords
    vals = set()
    for i in range(g.n_frames):
        g.seek(i)
        vals.add(tuple(np.array(g.convert("RGB"))[y, x]))
    if len(vals) != 1:
        ok = False
        print(f"  FAIL  {name} varies across frames: {vals}")

print(f"{OUT}: {OW}x{OH} ({SCALE}x), {len(frames)} frames, {sum(durs)/1000:.1f}s, "
      f"{os.path.getsize(p(OUT))/1024/1024:.2f} MB")
print(f"distinct colors across all frames: {len(allc)} (must be <= {PALETTE_N})")
print("static-pixel probes:", "PASS" if ok and len(allc) <= PALETTE_N else "FAIL")
