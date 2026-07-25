"""Build camo-test.svg — the one thing that gates the whole tracker architecture.

Tests three things at once, all of which the real tracker SVG depends on:
  1. Does GitHub's camo proxy preserve SMIL <animate>?          -> the moving bar
  2. Does it preserve a clipPath window stepping a sprite sheet? -> Claw'd typing
  3. Does an embedded base64 <image> survive with crisp edges?   -> image-rendering
If any of these render as a still frame in the README, we fall back to a GIF.
"""
import base64, io
import numpy as np
from PIL import Image

FRAMES, FW, FH = 5, 64, 56
BG = '#0D1117'

sheet = Image.open('typing_native.png').convert('RGB').crop((0, 0, FRAMES * FW, FH))
a = np.asarray(sheet).astype(int)
# key the near-white background out
white = (a[:, :, 0] > 225) & (a[:, :, 1] > 225) & (a[:, :, 2] > 225)
rgba = np.dstack([a, np.where(white, 0, 255)]).astype(np.uint8)

buf = io.BytesIO()
Image.fromarray(rgba).save(buf, format='PNG', optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode()

SCALE = 3
W, H = 420, FH * SCALE + 40
sw, sh = FRAMES * FW * SCALE, FH * SCALE
dur = 0.85  # 5 frames @ 170ms

keys = ';'.join(str(-i * FW * SCALE) for i in range(FRAMES + 1))
times = ';'.join(f'{i / FRAMES:.4f}' for i in range(FRAMES + 1))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="camo animation test">
  <rect width="100%" height="100%" fill="{BG}"/>

  <!-- TEST 1: sprite-sheet stepping through a clipPath window -->
  <clipPath id="win"><rect x="0" y="0" width="{FW * SCALE}" height="{sh}"/></clipPath>
  <g transform="translate(14,10)" clip-path="url(#win)">
    <image xlink:href="data:image/png;base64,{b64}"
           x="0" y="0" width="{sw}" height="{sh}"
           image-rendering="pixelated" style="image-rendering:pixelated">
      <animate attributeName="x" dur="{dur}s" repeatCount="indefinite"
               calcMode="discrete" values="{keys}" keyTimes="{times}"/>
    </image>
  </g>

  <!-- TEST 2: plain SMIL on a shape -->
  <rect x="220" y="30" width="14" height="14" fill="#F2711C">
    <animate attributeName="x" dur="1.6s" repeatCount="indefinite"
             values="220;380;220" calcMode="linear"/>
  </rect>

  <!-- TEST 3: SMIL driving an attribute other than position -->
  <circle cx="240" cy="80" r="7" fill="#3FB950">
    <animate attributeName="opacity" dur="1.2s" repeatCount="indefinite"
             values="1;0.1;1"/>
  </circle>

  <text x="264" y="86" font-family="monospace" font-size="13" fill="#8B949E">
    if these move, SMIL survives camo
  </text>
</svg>'''

open('camo-test.svg', 'w').write(svg)
print('camo-test.svg', len(svg) // 1024, 'KB')
