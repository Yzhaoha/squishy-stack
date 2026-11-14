#!/usr/bin/env python3
"""Build the Poki version from the test build (index.html at the repo root).

- adds the Poki SDK script to <head>
- BUILD='test' -> BUILD='poki' (no SDK = rewarded ads give no reward)
- strips the /*TEST*/ ... /*ENDTEST*/ hooks (?auto, window.__sq)

Writes poki/index.html and build/squishy-stack-poki.zip (index.html at the zip root).
"""
import os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SDK = '<script src="https://game-cdn.poki.com/scripts/v2/poki-sdk.js"></script>'

src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
out = src
assert out.count('<title>') == 1 and out.count("const BUILD='test';") == 1
out = out.replace('<title>', SDK + '\n<title>', 1)
out = out.replace("const BUILD='test';", "const BUILD='poki';", 1)
out, n = re.subn(r'/\*TEST\*/.*?/\*ENDTEST\*/\n?', '', out, flags=re.S)
assert n == 1, 'test block not found'
assert '__sq' not in out and 'G.auto=true' not in out
urls = set(re.findall(r'https?://[^"\'\s)<>]+', out))
assert urls == {'https://game-cdn.poki.com/scripts/v2/poki-sdk.js'}, urls

os.makedirs(os.path.join(ROOT, 'poki'), exist_ok=True)
open(os.path.join(ROOT, 'poki', 'index.html'), 'w', encoding='utf-8').write(out)
os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
zp = os.path.join(ROOT, 'build', 'squishy-stack-poki.zip')
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('index.html', out)
print('poki/index.html', len(out), 'bytes;', zp)
