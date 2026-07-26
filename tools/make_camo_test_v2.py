"""Build camo-test-v2.svg — four animation techniques, one per labelled box.

Section 0 of HANDOFF.md: the tracker architecture depends on which of these
survives GitHub's camo proxy. v1 was the wrong file and had an off-by-one in the
sprite offsets (a 6th value of -960 parked the whole sheet outside the window).

  Box 1  <animate> on a rect's x                  baseline: does SMIL run at all
  Box 2  <animate calcMode="discrete"> on image x  frame stepping, no interpolation
  Box 3  clipPath window + <animateTransform>      *** the mechanism the tracker needs
  Box 4  CSS @keyframes + steps()                  fallback if SMIL is stripped

Read the result on github.com/Mr-Shine09, not a local preview — camo only sits in
front of rendered pages.
"""
import base64, io
import numpy as np
from PIL import Image

FRAMES, SRC_W, SRC_H = 5, 64, 56
PAD_X, CONTENT_H = 4, 40                 # sprite content occupies rows 0-36
FW, FH = SRC_W + 2 * PAD_X, CONTENT_H    # padded cell, so the window edge is visible
SCALE = 3
BW, BH = FW * SCALE, FH * SCALE          # box interior = exactly one frame
SW = FRAMES * FW * SCALE                 # full sheet width when scaled
DUR = 0.85                               # 5 frames @ 170ms
BG, PANEL, EDGE, LABEL = '#0D1117', '#161B22', '#30363D', '#8B949E'

# The source strip packs its frames edge to edge, so a bare 64px window shows a
# sprite touching both walls and you cannot tell a correct clip from a bleed.
# Re-lay the cells with transparent gutters.
src = np.asarray(Image.open('typing_native.png').convert('RGB')).astype(int)
white = (src[:, :, 0] > 225) & (src[:, :, 1] > 225) & (src[:, :, 2] > 225)
src_rgba = np.dstack([src, np.where(white, 0, 255)]).astype(np.uint8)
strip = Image.fromarray(src_rgba)

sheet = Image.new('RGBA', (FRAMES * FW, FH), (0, 0, 0, 0))
for i in range(FRAMES):
    cell = strip.crop((i * SRC_W, 0, (i + 1) * SRC_W, CONTENT_H))
    sheet.paste(cell, (i * FW + PAD_X, 0))

buf = io.BytesIO()
sheet.save(buf, format='PNG', optimize=True)
B64 = base64.b64encode(buf.getvalue()).decode()

# 5 offsets, 5 keyTimes. The sheet must never leave the window.
OFFSETS = [-i * FW * SCALE for i in range(FRAMES)]
VALUES = ';'.join(str(v) for v in OFFSETS)
KEYTIMES = ';'.join(f'{i / FRAMES:.2f}' for i in range(FRAMES))

PAD, GAP, LBL = 14, 24, 26
COL = [PAD, PAD + BW + GAP]
ROW = [PAD + LBL, PAD + LBL + BH + GAP + LBL]
W = COL[1] + BW + PAD
H = ROW[1] + BH + PAD


def img(extra=''):
    return (f'<image xlink:href="data:image/png;base64,{B64}" x="0" y="0" '
            f'width="{SW}" height="{BH}" image-rendering="pixelated" '
            f'style="image-rendering:pixelated" {extra}')


def box(n, cx, cy, title, body):
    return f'''
  <!-- BOX {n}: {title} -->
  <text x="{cx}" y="{cy - 8}" font-family="monospace" font-size="12" fill="{LABEL}">{n}. {title}</text>
  <rect x="{cx - 1}" y="{cy - 1}" width="{BW + 2}" height="{BH + 2}" fill="{PANEL}" stroke="{EDGE}"/>
  <g transform="translate({cx},{cy})" clip-path="url(#win{n})">{body}
  </g>'''


clips = ''.join(f'<clipPath id="win{n}"><rect x="0" y="0" width="{BW}" '
                f'height="{BH}"/></clipPath>' for n in range(1, 5))

# 1 — baseline. A plain rect sliding on x. If this is frozen, SMIL is gone entirely.
b1 = f'''
    <rect x="8" y="{BH // 2 - 10}" width="20" height="20" fill="#F2711C">
      <animate attributeName="x" dur="1.6s" repeatCount="indefinite"
               values="8;{BW - 28};8" calcMode="linear"/>
    </rect>
    <circle cx="{BW - 24}" cy="24" r="8" fill="#3FB950">
      <animate attributeName="opacity" dur="1.2s" repeatCount="indefinite" values="1;0.1;1"/>
    </circle>'''

# 2 — discrete stepping of the image's own x attribute.
b2 = f'''
    {img()}>
      <animate attributeName="x" dur="{DUR}s" repeatCount="indefinite"
               calcMode="discrete" values="{VALUES}" keyTimes="{KEYTIMES}"/>
    </image>'''

# 3 — the tracker's mechanism: static image, animateTransform on the wrapping <g>.
b3 = f'''
    <g>
      <animateTransform attributeName="transform" type="translate" additive="sum"
                        dur="{DUR}s" repeatCount="indefinite" calcMode="discrete"
                        values="{';'.join(f'{v},0' for v in OFFSETS)}" keyTimes="{KEYTIMES}"/>
      {img()}/>
    </g>'''

# 4 — CSS. Note: may be suppressed by OS "reduce motion" even when SMIL runs.
b4 = f'''
    <g class="css-step">
      {img()}/>
    </g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="camo animation test v2: four techniques">
  <style>
    @keyframes sheet-step {{
      from {{ transform: translateX(0px); }}
      to   {{ transform: translateX(-{SW}px); }}
    }}
    .css-step {{ animation: sheet-step {DUR}s steps({FRAMES}) infinite; }}
  </style>
  <defs>{clips}</defs>
  <rect width="100%" height="100%" fill="{BG}"/>
{box(1, COL[0], ROW[0], 'animate on x (baseline)', b1)}
{box(2, COL[1], ROW[0], 'animate calcMode=discrete', b2)}
{box(3, COL[0], ROW[1], 'clipPath + animateTransform', b3)}
{box(4, COL[1], ROW[1], 'CSS @keyframes steps()', b4)}
</svg>
'''

open('../camo-test-v2.svg', 'w').write(svg)
print(f'camo-test-v2.svg  {W}x{H}  {len(svg) // 1024} KB')
print('offsets:', OFFSETS)
