#!/usr/bin/env python3
"""build_tracker.py -- renders tracker.svg from GitHub contribution data.

Run by .github/workflows/tracker.yml on a daily cron. Reads stats from
stdin as JSON (see fetch_contributions.py) and writes tracker.svg.

Everything the SVG needs is embedded: the pixel font is subset and
base64'd so it renders identically for someone who has never installed
it, and Claw'd is a base64 PNG sprite sheet stepped by SMIL through a
clipPath window. The Action only ever changes numbers and heatmap
cells -- it never touches the animation block.
"""
import base64, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).parent
FONT_SRC = HERE / 'ps2p.ttf'
CLAWD_SRC = HERE / 'typing_native.png'

BG = '#0D1117'
BORDER = '#21262D'
DIM = '#6E7681'
KEY = '#7D8590'
STR = '#A5D6FF'
NUM = '#79C0FF'
PUNC = '#484F58'
ACCENT = '#F2711C'

# GitHub-ish contribution ramp, but warmed to match Claw'd
RAMP = ['#161B22', '#4A2A12', '#8A4A18', '#C4621C', '#F2711C']

W, H = 600, 300
CH = 10                      # Press Start 2P is a strict square grid
LINE = 18
FRAMES, FW, FH = 5, 64, 56


def embed_font(text):
    """Subset to just the glyphs used, so the SVG stays small."""
    font = TTFont(str(FONT_SRC))
    subsetter = subset.Subsetter(subset.Options(layout_features=['*'], notdef_outline=True))
    subsetter.populate(text=''.join(sorted(set(text))))
    subsetter.subset(font)
    buf = io.BytesIO()
    font.flavor = 'woff2'
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def embed_clawd():
    sheet = Image.open(CLAWD_SRC).convert('RGB').crop((0, 0, FRAMES * FW, FH))
    a = np.asarray(sheet).astype(int)
    white = (a[:, :, 0] > 225) & (a[:, :, 1] > 225) & (a[:, :, 2] > 225)
    rgba = np.dstack([a, np.where(white, 0, 255)]).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(rgba).save(buf, format='PNG', optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def json_lines(d):
    """The card body, as syntax-coloured pseudo-JSON tspans."""
    rows = [
        ('{', None, None),
        ('user', f'"{d["user"]}"', 'str'),
        ('current_streak', str(d['current_streak']), 'num'),
        ('longest_streak', str(d['longest_streak']), 'num'),
        ('this_year', str(d['this_year']), 'num'),
        ('window', '"12 weeks"', 'str'),
        ('}', None, None),
    ]
    out = []
    for i, (k, v, kind) in enumerate(rows):
        y = 42 + i * LINE
        if v is None:
            out.append(f'<text x="20" y="{y}" fill="{PUNC}">{esc(k)}</text>')
            continue
        comma = ',' if i < len(rows) - 2 else ''
        col = NUM if kind == 'num' else STR
        out.append(
            f'<text x="20" y="{y}">'
            f'<tspan fill="{KEY}">  "{esc(k)}"</tspan>'
            f'<tspan fill="{PUNC}">: </tspan>'
            f'<tspan fill="{col}">{esc(v)}</tspan>'
            f'<tspan fill="{PUNC}">{comma}</tspan></text>'
        )
    return '\n  '.join(out)


def heatmap(weeks, x0, y0, cell=11, gap=3):
    """weeks: 12 lists of 7 ints, each 0-4."""
    out = []
    for wi, week in enumerate(weeks):
        for di, lvl in enumerate(week):
            x = x0 + wi * (cell + gap)
            y = y0 + di * (cell + gap)
            out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                       f'fill="{RAMP[max(0, min(4, lvl))]}"/>')
    return '\n  '.join(out)


def build(d):
    alive = d['current_streak'] > 0
    body = json_lines(d)

    # everything that ends up inside a <text>, so the subset covers it
    used = ''.join(str(v) for v in d.values()) + \
        'usercurrent_streaklongest_streakthis_yearwindow12 weeks{}",: ' + \
        'contributionsMonWedFrilastweeksdozingtypingstreak'
    font_b64 = embed_font(used)
    clawd_b64 = embed_clawd()

    hm = heatmap(d['weeks'], 20, 190)

    scale = 2
    sw, sh = FRAMES * FW * scale, FH * scale
    cx, cy = 420, 176
    dur = 0.85 if alive else 2.4          # dozing = same loop, much slower
    keys = ';'.join(str(-i * FW * scale) for i in range(FRAMES + 1))
    times = ';'.join(f'{i / FRAMES:.4f}' for i in range(FRAMES + 1))
    caption = 'streak alive' if alive else 'dozing...'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="contribution tracker: {d['current_streak']} day current streak, {d['longest_streak']} day longest">
  <defs>
    <style>
      @font-face {{
        font-family: 'PS2P';
        src: url(data:font/woff2;base64,{font_b64}) format('woff2');
      }}
      text {{ font-family: 'PS2P', monospace; font-size: {CH}px; }}
      .sm {{ font-size: 8px; fill: {DIM}; }}
    </style>
    <clipPath id="clawdwin">
      <rect x="{cx}" y="{cy}" width="{FW * scale}" height="{sh}"/>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" rx="8" fill="{BG}" stroke="{BORDER}"/>
  <text x="20" y="24" class="sm">~/Mr-Shine09/contributions</text>

  {body}

  {hm}
  <text x="20" y="{190 + 7 * 14 + 14}" class="sm">12 weeks ago</text>
  <text x="188" y="{190 + 7 * 14 + 14}" class="sm" text-anchor="end">today</text>

  <g clip-path="url(#clawdwin)">
    <image xlink:href="data:image/png;base64,{clawd_b64}"
           x="{cx}" y="{cy}" width="{sw}" height="{sh}"
           image-rendering="pixelated" style="image-rendering:pixelated">
      <animate attributeName="x" dur="{dur}s" repeatCount="indefinite"
               calcMode="discrete" values="{';'.join(str(cx + int(k)) for k in keys.split(';'))}"
               keyTimes="{times}"/>
    </image>
  </g>
  <text x="{cx + FW}" y="{cy + sh + 16}" class="sm" text-anchor="middle">{caption}</text>
</svg>'''


if __name__ == '__main__':
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('tracker.svg')
    data = json.load(sys.stdin)
    svg = build(data)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(f'{out}  {W}x{H}  {len(svg) // 1024}KB  '
          f'streak={data["current_streak"]}')
