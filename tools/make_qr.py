#!/usr/bin/env python3
"""Dependency-free QR generator (byte mode, ECC level M, versions 1-5).
Usage:  python tools/make_qr.py https://mayadafarhan.github.io/
Writes qr/mayada-card-qr.svg and qr/mayada-card-qr.png (PNG needs Pillow)."""
import sys, os

URL = sys.argv[1] if len(sys.argv) > 1 else "https://mayadafarhan.github.io/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "qr")

# --- Reed-Solomon over GF(256) ---
EXP, LOG = [0] * 512, [0] * 256
x = 1
for i in range(255):
    EXP[i], LOG[x] = x, i
    x <<= 1
    if x & 0x100: x ^= 0x11D
for i in range(255, 512): EXP[i] = EXP[i - 255]
mul = lambda a, b: 0 if not a or not b else EXP[LOG[a] + LOG[b]]

def rs(data, n):
    g = [1]
    for i in range(n):
        ng = [0] * (len(g) + 1)
        for j, c in enumerate(g):
            ng[j] ^= c; ng[j + 1] ^= mul(c, EXP[i])
        g = ng
    r = [0] * n
    for b in data:
        f = b ^ r[0]; r = r[1:] + [0]
        for i in range(n): r[i] ^= mul(g[i + 1], f)
    return r

# version: (data codewords per block, EC codewords per block, blocks) at level M
VER = {1: (16, 10, 1), 2: (28, 16, 1), 3: (44, 26, 1), 4: (32, 18, 2), 5: (43, 24, 2)}
ALIGN = {2: 18, 3: 22, 4: 26, 5: 30}

def build(text):
    raw = text.encode()
    v = next((v for v, (d, e, b) in VER.items() if d * b - 2 >= len(raw)), None)
    if not v: sys.exit("URL too long for this generator (max ~84 characters).")
    d, e, nb = VER[v]; cap = d * nb
    bits = "0100" + format(len(raw), "08b") + "".join(format(c, "08b") for c in raw)
    bits += "0" * min(4, cap * 8 - len(bits)); bits += "0" * (-len(bits) % 8)
    cw = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
    k = 0
    while len(cw) < cap: cw.append((0xEC, 0x11)[k % 2]); k += 1
    blocks = [cw[i * d:(i + 1) * d] for i in range(nb)]
    ecs = [rs(b, e) for b in blocks]
    final = [b[i] for i in range(d) for b in blocks] + [c[i] for i in range(e) for c in ecs]
    stream = "".join(format(c, "08b") for c in final) + "0" * 7

    n = 17 + 4 * v
    M = [[False] * n for _ in range(n)]; F = [[False] * n for _ in range(n)]
    def put(xx, yy, val):
        if 0 <= xx < n and 0 <= yy < n: M[yy][xx] = val; F[yy][xx] = True
    for cx, cy in ((3, 3), (n - 4, 3), (3, n - 4)):           # finders + separators
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                put(cx + dx, cy + dy, max(abs(dx), abs(dy)) not in (2, 4))
    for i in range(n):                                        # timing patterns
        if not F[i][6]: put(6, i, i % 2 == 0)
        if not F[6][i]: put(i, 6, i % 2 == 0)
    if v in ALIGN:
        a = ALIGN[v]
        for dy in range(-2, 3):
            for dx in range(-2, 3): put(a + dx, a + dy, max(abs(dx), abs(dy)) != 1)

    def draw_fmt(G, mask):
        r = mask << 10
        for i in range(14, 9, -1):
            if r >> i & 1: r ^= 0x537 << (i - 10)
        b = ((mask << 10) | r) ^ 0x5412
        g = lambda i: bool(b >> i & 1)
        def s(xx, yy, val): G[yy][xx] = val; F[yy][xx] = True
        for i in range(6): s(8, i, g(i))
        s(8, 7, g(6)); s(8, 8, g(7)); s(7, 8, g(8))
        for i in range(9, 15): s(14 - i, 8, g(i))
        for i in range(8): s(n - 1 - i, 8, g(i))
        for i in range(8, 15): s(8, n - 15 + i, g(i))
        s(8, n - 8, True)
    draw_fmt(M, 0)
    base = [r[:] for r in M]

    path, up, right = [], True, n - 1                          # zig-zag data placement
    while right >= 1:
        if right == 6: right = 5
        for j in range(n):
            y = n - 1 - j if up else j
            for xx in (right, right - 1):
                if not F[y][xx]: path.append((xx, y))
        up = not up; right -= 2
    masks = [lambda r, c: (r + c) % 2 == 0, lambda r, c: r % 2 == 0, lambda r, c: c % 3 == 0,
             lambda r, c: (r + c) % 3 == 0, lambda r, c: (r // 2 + c // 3) % 2 == 0,
             lambda r, c: (r * c) % 2 + (r * c) % 3 == 0, lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
             lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0]
    def penalty(G):
        p = 0
        for g in (G, [list(c) for c in zip(*G)]):
            for row in g:
                run = 1
                for i in range(1, n):
                    if row[i] == row[i - 1]:
                        run += 1
                        if run == 5: p += 3
                        elif run > 5: p += 1
                    else: run = 1
                s = "".join("1" if c else "0" for c in row)
                p += 40 * (s.count("10111010000") + s.count("00001011101"))
        for y in range(n - 1):
            for xx in range(n - 1):
                if G[y][xx] == G[y][xx + 1] == G[y + 1][xx] == G[y + 1][xx + 1]: p += 3
        return p + 10 * (abs(sum(map(sum, G)) * 100 // (n * n) - 50) // 5)
    best = None
    for mi, mf in enumerate(masks):
        G = [r[:] for r in base]
        for i, (xx, y) in enumerate(path):
            G[y][xx] = (stream[i] == "1" if i < len(stream) else False) ^ mf(y, xx)
        draw_fmt(G, mi)
        sc = penalty(G)
        if best is None or sc < best[0]: best = (sc, G)
    return best[1]

grid = build(URL); n = len(grid); Q = 4
os.makedirs(OUT, exist_ok=True)
rects = "".join(f"M{x + Q},{y + Q}h1v1h-1z" for y in range(n) for x in range(n) if grid[y][x])
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n + 2 * Q} {n + 2 * Q}" shape-rendering="crispEdges">'
       f'<title>QR code for {URL}</title><rect width="100%" height="100%" fill="#fff"/><path fill="#0b1230" d="{rects}"/></svg>')
open(os.path.join(OUT, "mayada-card-qr.svg"), "w").write(svg)
try:
    from PIL import Image
    S = 24; im = Image.new("RGB", ((n + 2 * Q) * S,) * 2, "white"); px = im.load()
    for y in range(n):
        for x in range(n):
            if grid[y][x]:
                for dy in range(S):
                    for dx in range(S): px[(x + Q) * S + dx, (y + Q) * S + dy] = (11, 18, 48)
    im.save(os.path.join(OUT, "mayada-card-qr.png"))
except ImportError:
    print("Pillow not installed: PNG skipped (pip install pillow).")
print(f"QR for {URL} -> version {(n - 17) // 4}, saved in qr/")
