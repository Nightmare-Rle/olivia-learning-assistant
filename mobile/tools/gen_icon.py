# Generate OLIVIA launcher icon (rounded-square gradient + white "O" ring) as PNGs.
# Pure stdlib (zlib) PNG writer.
import os, struct, zlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "android")

TOP = (46, 134, 193)    # #2E86C1
BOT = (31, 80, 118)     # darkened #1F5076
RING = (255, 255, 255)


def write_png(path, w, h, rgba_rows):
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    raw = b"".join(b"\x00" + bytes(row) for row in rgba_rows)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def rounded(x, y, w, h, r, px, py):
    if px < x + r and py < y + r:
        return (px - (x + r)) ** 2 + (py - (y + r)) ** 2 <= r * r
    if px > x + w - r - 1 and py < y + r:
        return (px - (x + w - r - 1)) ** 2 + (py - (y + r)) ** 2 <= r * r
    if px < x + r and py > y + h - r - 1:
        return (px - (x + r)) ** 2 + (py - (y + h - r - 1)) ** 2 <= r * r
    if px > x + w - r - 1 and py > y + h - r - 1:
        return (px - (x + w - r - 1)) ** 2 + (py - (y + h - r - 1)) ** 2 <= r * r
    return x <= px < x + w and y <= py < y + h


def render(size):
    cx = cy = size / 2.0
    outer = size * 0.36
    thick = size * 0.10
    inner = outer - thick
    pad = size * 0.06
    r = size * 0.20
    rows = []
    for y in range(size):
        row = []
        t = y / max(1, size - 1)
        for x in range(size):
            if not rounded(pad, pad, size - 2 * pad, size - 2 * pad, r, x, y):
                row += [0, 0, 0, 0]
                continue
            rr = ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5
            if inner <= rr <= outer:
                row += [RING[0], RING[1], RING[2], 255]
            else:
                row += [int(TOP[0] + (BOT[0] - TOP[0]) * t),
                        int(TOP[1] + (BOT[1] - TOP[1]) * t),
                        int(TOP[2] + (BOT[2] - TOP[2]) * t), 255]
        rows.append(row)
    return rows


def main():
    dirs = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    for d, size in dirs.items():
        folder = os.path.join(OUT, "res", "mipmap-" + d)
        os.makedirs(folder, exist_ok=True)
        write_png(os.path.join(folder, "ic_launcher.png"), size, size, render(size))
        print("wrote", os.path.join(folder, "ic_launcher.png"))
    print("ICON OK")


if __name__ == "__main__":
    main()