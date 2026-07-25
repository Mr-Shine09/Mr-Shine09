"""avatar-idle.gif — layered cutout idle derived from ONE sprite.

Layers: head (rows 0-21) and body (rows 22+) offset independently.
Head lags the body by one frame; that lag is what reads as alive.
Neck gap from the lag is filled by duplicating the top neck row.
Blink = the glasses bar thickens by one row for a single frame.
Speech bubble is baked in so it can never drift or reflow on mobile.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SPRITE = 'avatar_native.png'
FONT = 'ps2p.ttf'
OUT = 'avatar-idle.gif'
SCALE = 4
MS = 250

NECK_SPLIT = 22          # first row of the body layer
NECK_ROW = 20            # row duplicated to fill the gap when the head rides high
EYE_ROW, EYE_X0, EYE_X1 = 12, 9, 25

CREAM = (240, 240, 230, 255)
INK = (27, 31, 36, 255)

LINES = [
    'Hi, my name',
    'is Oak - a',
    'Computer',
    'Engineering/',
    'Science',
    'student at',
    'De Anza',
    'College.',
]

# 16 frames @ 250ms = 4s loop. Bob repeats every 4; blink fires once.
BOB = [0, -1, 0, 1] * 4
BLINK_FRAME = 9

spr = np.asarray(Image.open(SPRITE).convert('RGBA'))
SH, SW = spr.shape[:2]

PAD_X, PAD_Y, LEAD = 5, 5, 3
CH = 8
bw = max(len(s) for s in LINES) * CH + PAD_X * 2 + 2
bh = len(LINES) * CH + (len(LINES) - 1) * LEAD + PAD_Y * 2 + 2
GAP = 6
W, H = SW + GAP + bw, SH
BX, BY = SW + GAP, 2

font = ImageFont.truetype(FONT, CH)


def bubble_layer():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([BX, BY, BX + bw - 1, BY + bh - 1], fill=CREAM, outline=INK)
    # tail: solid wedge pointing back at the head, no anti-aliasing
    for i in range(GAP):
        x = BX - 1 - i
        d.line([(x, 11 + i), (x, 17 - i)], fill=CREAM)
        d.point((x, 10 + i), fill=INK)
        d.point((x, 18 - i), fill=INK)
    for n, line in enumerate(LINES):
        d.text((BX + PAD_X + 1, BY + PAD_Y + 1 + n * (CH + LEAD)), line,
               font=font, fill=INK)
    return np.asarray(img).copy()


BUBBLE = bubble_layer()


def compose(i):
    body_dy = BOB[i]
    head_dy = body_dy                          # head locked to the body, no lag
    canvas = np.zeros((H, W, 4), dtype=np.uint8)

    def blit(src, dy, y0, y1):
        for y in range(y0, y1):
            ty = y + dy
            if 0 <= ty < H:
                row = src[y]
                m = row[:, 3] > 0
                canvas[ty, :SW][m] = row[m]

    blit(spr, body_dy, NECK_SPLIT, SH)
    blit(spr, head_dy, 0, NECK_SPLIT)

    # head rode higher than the torso -> 1px of bare neck. Duplicate it.
    if head_dy < body_dy:
        ty = NECK_SPLIT + head_dy
        row = spr[NECK_ROW]
        m = row[:, 3] > 0
        if 0 <= ty < H:
            canvas[ty, :SW][m] = row[m]

    if i == BLINK_FRAME:
        y = EYE_ROW + head_dy
        src = canvas[y, EYE_X0:EYE_X1]
        dst = canvas[y + 1, EYE_X0:EYE_X1]
        dark = (src[:, :3].sum(1) < 200) & (src[:, 3] > 0) & (dst[:, 3] > 0)
        dst[dark] = src[dark]

    m = BUBBLE[:, :, 3] > 0
    canvas[m] = BUBBLE[m]
    return canvas


frames = [compose(i) for i in range(len(BOB))]

# one global palette across every frame -- animated GIFs share a single colour
# table, and per-frame ADAPTIVE is exactly the bug that broke the Claw'd build.
stack = Image.fromarray(np.vstack([f[:, :, :3] for f in frames]))
master = stack.quantize(colors=255, method=Image.MEDIANCUT, dither=Image.NONE)

# pin index 255 as the transparency slot and force the SAME 256-entry palette
# onto every frame, so the transparent index can never be remapped mid-loop
pal = list(master.getpalette()[:255 * 3]) + [255, 0, 255]

out = []
for f in frames:
    img = Image.fromarray(f[:, :, :3]).resize((W * SCALE, H * SCALE), Image.NEAREST)
    q = img.quantize(palette=master, dither=Image.NONE)
    alpha = Image.fromarray(f[:, :, 3]).resize((W * SCALE, H * SCALE), Image.NEAREST)
    q.paste(255, mask=Image.eval(alpha, lambda v: 255 - v))
    q.putpalette(pal)
    out.append(q)

out[0].save(OUT, save_all=True, append_images=out[1:], duration=MS,
            loop=0, disposal=2, transparency=255, optimize=False)

print(f'{OUT}  {W * SCALE}x{H * SCALE}  {len(out)} frames  {MS}ms')

# static contact sheet so the bob/lag/blink can be inspected frame by frame
sheet = Image.new('RGB', (W * len(frames), H), (13, 17, 23))
for n, f in enumerate(frames):
    im = Image.fromarray(f)
    sheet.paste(im, (n * W, 0), im)
sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save('idle_sheet.png')
