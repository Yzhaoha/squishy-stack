#!/usr/bin/env python3
"""Crop the character art in art/characters/*.png and embed it into index.html.

For every <id>.png (id = SPECIES id in index.html):
- crop the empty border (alpha > 40)
- find the "body box" (the part that should fill the collision box w x h;
  ears, gills, fins stick out of it)
- find the two bead eyes (for blinking)
- resize, encode as WebP, base64 -> written between /*ART*/ and /*ENDART*/

Characters without a PNG keep the old code-drawn look.

Usage: python3 tools/embed_art.py [--debug DIR]   (needs Pillow + numpy)
"""
import base64, io, json, os, re, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'art', 'characters')
OUT_W = 400        # px width of the embedded image
QUALITY = 80
BLINK = False     # the pastel style has big sparkly eyes; a painted-over blink looks wrong
# manual fixes per id if the automatic body box / eyes are off: {'id': {'L':..,'R':..,'top':..}}
OVERRIDE = {}


def longest_run(col):
    best = cur = 0
    for v in col:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


def analyse(path, box_w, box_h, ov):
    box_ratio = box_w / box_h
    im = Image.open(path).convert('RGBA')
    A = np.array(im)
    ys, xs = np.where(A[:, :, 3] > 40)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    im = im.crop((x0, y0, x1, y1))
    A = A[y0:y1, x0:x1]
    a = A[:, :, 3] > 40
    rgb = A[:, :, :3].astype(int)
    H, W = a.shape
    roww = a.sum(1)
    top = np.argmax(roww >= 0.5 * roww.max()) / H           # skip ears / fins on top
    runs = np.array([longest_run(a[:, i]) for i in range(W)])
    ok = np.where(runs >= 0.55 * runs.max())[0]              # skip gills / rounded sides
    L, R = ok.min() / W, (ok.max() + 1) / W
    top, L, R = ov.get('top', top), ov.get('L', L), ov.get('R', R)
    bot = 0.99
    # fit body box to the collision box: split the mismatch between a little
    # sideways overhang and a little vertical stretch
    e = ((R - L) * W) / ((bot - top) * H) / box_ratio
    kx = min(max(e ** 0.5, 0.93), 1.08)
    # if the art is much taller / flatter than the collision box, change the box height instead of squeezing the picture
    new_h = None
    if abs(e / kx - 1) > 0.04:
        new_h = round(box_w * kx / (((R - L) * W) / ((bot - top) * H)))
    dw = kx / (R - L)
    dx = -kx / 2 - L * dw
    dh = 1 / (bot - top)
    dy = -1 - top * dh
    # eyes: dark blobs left and right of the centre (the mouth is in the middle)
    dark = (rgb.sum(2) < 180) & a
    eyes = []
    for sl in (slice(0, int(.43 * W)), slice(int(.57 * W), W)):
        yy, xx = np.where(dark[:, sl])
        if len(xx) < 200:
            continue
        xx = xx + sl.start
        cx, cy = np.median(xx), np.median(yy)
        keep = (abs(xx - cx) < 0.06 * W) & (abs(yy - cy) < 0.06 * W)
        xx, yy = xx[keep], yy[keep]
        r = (len(xx) / np.pi) ** 0.5
        cx, cy = xx.mean(), yy.mean()
        # skin colour: ring just outside the eye
        ring = []
        for ang in np.linspace(0, 2 * np.pi, 16, endpoint=False):
            px, py = int(cx + np.cos(ang) * r * 1.5), int(cy + np.sin(ang) * r * 1.5)
            if 0 <= px < W and 0 <= py < H and a[py, px] and rgb[py, px].sum() > 300:
                ring.append(rgb[py, px])
        skin = np.median(np.array(ring), 0).astype(int) if ring else np.array([255, 220, 200])
        eyes.append((cx / W, cy / H, r / W, '#%02x%02x%02x' % tuple(skin)))
    small = im.resize((OUT_W, round(OUT_W * H / W)), Image.LANCZOS)
    buf = io.BytesIO()
    small.save(buf, 'WEBP', quality=QUALITY, method=6)
    meta = {'d': [round(v, 4) for v in (dx, dy, dw, dh)], 'ar': round(W / H, 4)}
    if new_h:
        meta['h'] = new_h
    if BLINK and len(eyes) == 2:
        meta['e'] = [[round(e_[0], 4), round(e_[1], 4), round(e_[2], 4), e_[3]] for e_ in eyes]
    meta['u'] = 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
    dbg = dict(im=im, L=L, R=R, top=top, bot=bot, eyes=eyes, e=e, kx=kx, new_h=new_h, kb=len(buf.getvalue()))
    return meta, dbg


def main():
    dbg_dir = sys.argv[sys.argv.index('--debug') + 1] if '--debug' in sys.argv else None
    html_path = os.path.join(ROOT, 'index.html')
    html = open(html_path, encoding='utf-8').read()
    art = {}
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith('.png'):
            continue
        sid = fn[:-4]
        m = re.search(r"\{id:'%s',[^}]*?w:(\d+),h:(\d+)" % re.escape(sid), html)
        if not m:
            print('%-6s skipped (not a character id; props/backgrounds are handled separately)' % sid)
            continue
        w, h = int(m.group(1)), int(m.group(2))
        meta, d = analyse(os.path.join(SRC, fn), w, h, OVERRIDE.get(sid, {}))
        art[sid] = meta
        print('%-6s %4.1f KB  body/box ratio %.3f  overhang x%.3f  box h %s' % (sid, d['kb'] / 1024, d['e'], d['kx'], '%d -> %d' % (h, d['new_h']) if d['new_h'] else h))
        if dbg_dir:
            im = d['im'].copy()
            W, H = im.size
            bg = Image.new('RGBA', im.size, (120, 200, 255, 255))
            bg.alpha_composite(im)
            dr = ImageDraw.Draw(bg)
            dr.rectangle((d['L'] * W, d['top'] * H, d['R'] * W, d['bot'] * H), outline=(255, 0, 0, 255), width=5)
            for ex, ey, er, _ in d['eyes']:
                dr.ellipse(((ex - er) * W, ey * H - er * W, (ex + er) * W, ey * H + er * W), outline=(0, 255, 0, 255), width=4)
            bg.convert('RGB').resize((W // 2, H // 2)).save(os.path.join(dbg_dir, sid + '_debug.png'))
    block = '/*ART*/const ART=' + json.dumps(art, separators=(',', ':')) + ';/*ENDART*/'
    html, n = re.subn(r'/\*ART\*/.*?/\*ENDART\*/', lambda _: block, html, flags=re.S)
    assert n == 1, 'ART marker not found in index.html'
    open(html_path, 'w', encoding='utf-8').write(html)
    print('index.html', len(html.encode()) // 1024, 'KB,', len(art), 'characters with art')


if __name__ == '__main__':
    main()
