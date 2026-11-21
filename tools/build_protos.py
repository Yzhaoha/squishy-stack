#!/usr/bin/env python3
"""Build the two gameplay prototypes (proto-physics.html, proto-merge.html).

For each character used: crop the PNG (alpha > 40), compute a convex hull of the
opaque pixels (<= 14 vertices, in units of the cropped image width, centred on
the image centre), shrink to a small WebP. Inject those, a background, the base
and Matter.js into tools/proto/*.tpl.html.

Usage: python3 tools/build_protos.py   (needs Pillow + numpy)
"""
import base64, io, json, os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, 'art', 'characters')
PROTO = os.path.join(ROOT, 'tools', 'proto')

PHYS = ['shiba', 'bun', 'toast', 'boba', 'mush', 'cro', 'shark', 'pud']
MERGE = ['mochi', 'bun', 'frog', 'shiba', 'cat', 'bear', 'sloth', 'uni', 'dragon', 'gcapy']


def webp(im, w, q=80):
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'WEBP', quality=q, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def hull(pts):
    pts = sorted(set(pts))
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def simplify(h, n):
    h = list(h)
    while len(h) > n:
        best, bi = None, 0
        for i in range(len(h)):
            a, b, c = h[i - 1], h[i], h[(i + 1) % len(h)]
            ar = abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))
            if best is None or ar < best:
                best, bi = ar, i
        h.pop(bi)
    return h


def character(cid):
    im = Image.open(os.path.join(ART, cid + '.png')).convert('RGBA')
    A = np.array(im)[:, :, 3]
    ys, xs = np.where(A > 40)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    W, H = im.size
    a = np.array(im)[:, :, 3] > 128
    pts = []
    for y in range(0, H, 2):
        row = np.where(a[y])[0]
        if len(row):
            pts += [(row[0], y), (row[-1] + 1, y)]
    h = simplify(hull(pts), 14)
    v = [[round(x / W - 0.5, 4), round(y / W - H / W / 2, 4)] for x, y in h]
    return {'u': webp(im, 260), 'ar': round(W / H, 4), 'v': v}


def build(tpl, out, ids, bg):
    chars = {c: character(c) for c in ids}
    props = {'bg': webp(Image.open(os.path.join(ART, bg + '.png')).convert('RGB'), 540, 70)}
    base = Image.open(os.path.join(ART, 'base.png')).convert('RGBA')
    ys, xs = np.where(np.array(base)[:, :, 3] > 40)
    props['base'] = webp(base.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)), 400)
    s = open(os.path.join(PROTO, tpl), encoding='utf-8').read()
    matter = open(os.path.join(PROTO, 'matter.min.js'), encoding='utf-8').read()
    s = s.replace('/*MATTER*/', matter)
    s = s.replace('/*CHARS*/', 'const CHARS=' + json.dumps(chars, separators=(',', ':')) + ';')
    s = s.replace('/*PROPS*/', 'const PROPS=' + json.dumps(props, separators=(',', ':')) + ';')
    open(os.path.join(ROOT, out), 'w', encoding='utf-8').write(s)
    print(out, round(len(s) / 1024), 'KB')


if __name__ == '__main__':
    build('physics.tpl.html', 'proto-physics.html', PHYS, 'bg_pals')
    build('merge.tpl.html', 'proto-merge.html', MERGE, 'bg_cafe')
