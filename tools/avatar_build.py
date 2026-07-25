from PIL import Image
import numpy as np

SRC = 'Oak_sAvater.png'
NATIVE_H = 120         # figure height in native pixels
NCOLORS = 18

im = Image.open(SRC).convert('RGB')
a = np.asarray(im).astype(np.float64)

# ---- 1. patch out the club crest (trademark + unreadable at target size) ----
navy = np.array([37, 57, 103], dtype=np.float64)
a[296:398, 603:708] = navy

# ---- 1b. skin: pull blue up toward green (kills the yellow cast) + lighten ----
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
skin = (r > 115) & (r > b + 22) & (g > b + 8) & (g < r + 6)
b_new = b + 0.55 * (g - b)
a[:, :, 2] = np.where(skin, b_new, b)
for ch in range(3):
    a[:, :, ch] = np.where(skin, np.clip(a[:, :, ch] * 1.04, 0, 255), a[:, :, ch])

# ---- 2. magenta key + despill ----
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mag = (r > 190) & (g < 95) & (b > 190)
alpha = (~mag).astype(np.float64)

# despill: where magenta bleeds into edges, clamp the magenta channels toward green
spill = np.clip(np.minimum(r, b) - g, 0, None)
edge = (alpha > 0) & (spill > 45)
a[:, :, 0] = np.where(edge, r - spill * 0.8, r)
a[:, :, 2] = np.where(edge, b - spill * 0.8, b)

rgba = np.dstack([np.clip(a, 0, 255), alpha * 255]).astype(np.uint8)

# ---- 3. crop to figure ----
ys, xs = np.where(alpha > 0)
y0, y1 = ys.min(), ys.max() + 1
x0, x1 = xs.min(), xs.max() + 1
crop = rgba[y0:y1, x0:x1]
h, w = crop.shape[:2]
nw = max(1, round(w * NATIVE_H / h))

# ---- 4. area downsample with premultiplied alpha ----
c = crop.astype(np.float64)
al = c[:, :, 3:4] / 255.0
pm = np.dstack([c[:, :, :3] * al, c[:, :, 3]])
small = np.asarray(
    Image.fromarray(pm.astype(np.uint8)).resize((nw, NATIVE_H), Image.BOX)
).astype(np.float64)
sa = small[:, :, 3:4] / 255.0
rgb = np.divide(small[:, :, :3], np.where(sa > 0.02, sa, 1), where=True)
rgb = np.clip(rgb, 0, 255)

# hard alpha threshold -> crisp pixel edges, no semi-transparent fringe
hard = (sa[:, :, 0] > 0.45)

# ---- 5. quantize to a small palette (opaque pixels only) ----
flat = Image.fromarray(rgb.astype(np.uint8))
pal_img = flat.quantize(colors=NCOLORS, method=Image.MEDIANCUT, dither=Image.NONE)
q = np.asarray(pal_img.convert('RGB'))

out = np.dstack([q, (hard * 255).astype(np.uint8)])

# any pixel that still quantized to a magenta-ish colour is a keying remnant
qr, qg, qb = q[:, :, 0].astype(int), q[:, :, 1].astype(int), q[:, :, 2].astype(int)
remnant = (qr > qg + 40) & (qb > qg + 40)
out[:, :, 3][remnant] = 0
print('magenta remnants dropped', int(remnant.sum()))

Image.fromarray(out).save('avatar_native.png')

prev = Image.fromarray(out).resize((nw * 5, NATIVE_H * 5), Image.NEAREST)
bg = Image.new('RGB', prev.size, (13, 17, 23))
bg.paste(prev, (0, 0), prev)
bg.save('avatar_preview.png')

print('native size', nw, NATIVE_H)
print('unique colors', len(Image.fromarray(q).getcolors(999999)))
