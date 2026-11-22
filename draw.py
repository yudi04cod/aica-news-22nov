#!/usr/bin/env python3
"""Draw a newspaper front page summing up Sunday 22 November 2026.

All artwork is drawn with PIL shapes; no external images, no network.
Run: python3 draw.py  -> writes entry.png (1024x1024) next to this file.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
TEAL = (14, 110, 110)
GOLD = (184, 134, 11)
GREY = (90, 88, 82)
SKY = (176, 208, 232)
SEA = (46, 110, 160)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 5
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- illustrations

def draw_radar_scene(d, x, y, w, h):
    """Headline art: radar dish, missile arcs and a coastline over the Gulf."""
    d.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=2)
    # sea
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA)
    for i in range(5):
        yy = y + int(h * 0.68) + i * 12
        d.arc([x + 10, yy, x + w - 10, yy + 18], 200, 340, fill=(255, 255, 255), width=2)
    # coastline
    d.polygon([(x, y + h), (x, y + int(h * 0.55)), (x + int(w * 0.35), y + int(h * 0.48)),
               (x + int(w * 0.6), y + int(h * 0.58)), (x + w, y + int(h * 0.5)),
               (x + w, y + h)], fill=(214, 196, 150))
    # radar dish: filled half-ellipse on a mast
    cx, cy = x + int(w * 0.24), y + int(h * 0.40)
    d.line([(cx, cy), (cx, y + int(h * 0.62))], fill=INK, width=5)
    d.pieslice([cx - 46, cy - 52, cx + 46, cy + 20], 180, 360, fill=RED, outline=INK)
    d.line([(cx - 46, cy - 16), (cx + 46, cy - 16)], fill=INK, width=3)
    # missile arcs with small rockets riding them
    for k, (sx, ex) in enumerate([(0.52, 0.80), (0.40, 0.66)]):
        x0, x1 = x + int(w * sx), x + int(w * ex)
        y0 = y + int(h * 0.08) + k * 30
        d.arc([x0, y0, x1 + 80, y0 + 130], 200, 330, fill=(60, 60, 60), width=3)
        mx, my = x1 + 24, y0 + 40
        d.polygon([(mx, my - 14), (mx + 7, my + 2), (mx - 7, my + 2)], fill=RED)
        d.rectangle([mx - 4, my + 2, mx + 4, my + 14], fill=INK)
    # blast star near the dish
    bx, by = x + int(w * 0.56), y + int(h * 0.28)
    for ang in range(0, 360, 45):
        r = math.radians(ang)
        d.line([(bx, by), (bx + int(20 * math.cos(r)), by + int(20 * math.sin(r)))],
               fill=GOLD, width=4)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=GOLD, outline=RED, width=2)
    d.text((x + 10, y + h - 26), "BAHRAIN  •  GULF", font=font(SANS_B, 15), fill=(255, 255, 255))


def draw_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=2)
    d.rectangle([x, y + int(h * 0.66), x + w, y + h], fill=SEA)
    # hull + containers
    d.polygon([(x + 12, y + int(h * 0.55)), (x + w - 12, y + int(h * 0.55)),
               (x + w - 30, y + int(h * 0.72)), (x + 30, y + int(h * 0.72))], fill=(60, 60, 66))
    d.rectangle([x + 26, y + int(h * 0.34), x + 66, y + int(h * 0.55)], fill=RED)
    d.rectangle([x + 72, y + int(h * 0.34), x + 112, y + int(h * 0.55)], fill=GOLD)
    d.rectangle([x + 118, y + int(h * 0.40), x + 148, y + int(h * 0.55)], fill=TEAL)
    # drones above
    for dx, dy in [(0.30, 0.16), (0.62, 0.10), (0.82, 0.22)]:
        px, py = x + int(w * dx), y + int(h * dy)
        d.ellipse([px - 5, py - 4, px + 5, py + 4], fill=INK)
        d.line([(px - 12, py - 8), (px + 12, py - 8)], fill=INK, width=2)
        d.line([(px - 12, py + 8), (px + 12, py + 8)], fill=INK, width=2)
        d.line([(px, py + 4), (px, py + 22)], fill=RED, width=2)


def draw_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244), outline=INK, width=2)
    # ballot box
    d.rectangle([x + 22, y + int(h * 0.42), x + w - 22, y + int(h * 0.88)], fill=BLUE)
    d.rectangle([x + 14, y + int(h * 0.34), x + w - 14, y + int(h * 0.44)], fill=INK)
    d.rectangle([x + int(w * 0.42), y + int(h * 0.37), x + int(w * 0.58), y + int(h * 0.41)],
                fill=PAPER)
    # ballot paper going in, with a tick
    d.polygon([(x + int(w * 0.38), y + 8), (x + int(w * 0.72), y + 14),
               (x + int(w * 0.66), y + int(h * 0.40)), (x + int(w * 0.32), y + int(h * 0.34))],
              fill=(255, 255, 255), outline=INK)
    d.line([(x + int(w * 0.44), y + int(h * 0.22)), (x + int(w * 0.52), y + int(h * 0.30)),
            (x + int(w * 0.66), y + int(h * 0.10))], fill=TEAL, width=5)


def draw_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 228), outline=INK, width=2)
    # seismograph trace
    pts = [(x + 8, y + int(h * 0.42))]
    for i, amp in enumerate([0, 6, -8, 26, -46, 58, -30, 12, -6, 4, 0]):
        pts.append((x + 8 + (i + 1) * (w - 16) // 11, y + int(h * 0.42) + amp))
    d.line(pts, fill=RED, width=3, joint="curve")
    # cracked ground
    gy = y + int(h * 0.72)
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(150, 122, 88))
    d.line([(x + int(w * 0.30), gy), (x + int(w * 0.38), gy + 16),
            (x + int(w * 0.30), gy + 30), (x + int(w * 0.46), gy + 44)], fill=INK, width=3)
    d.line([(x + int(w * 0.68), gy), (x + int(w * 0.60), gy + 20),
            (x + int(w * 0.72), gy + 34)], fill=INK, width=3)
    d.text((x + 10, y + 8), "M 4.1", font=font(SANS_B, 22), fill=RED)


def draw_robot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244), outline=INK, width=2)
    # robot head
    hx, hy = x + w // 2, y + int(h * 0.52)
    d.rectangle([hx - 42, hy - 34, hx + 42, hy + 30], fill=(200, 205, 212), outline=INK, width=3)
    d.line([(hx, hy - 34), (hx, hy - 52)], fill=INK, width=3)
    d.ellipse([hx - 6, hy - 58, hx + 6, hy - 46], fill=RED)
    d.ellipse([hx - 26, hy - 14, hx - 8, hy + 4], fill=TEAL)
    d.ellipse([hx + 8, hy - 14, hx + 26, hy + 4], fill=TEAL)
    d.line([(hx - 18, hy + 18), (hx + 18, hy + 18)], fill=INK, width=3)
    # red ban circle over it
    d.ellipse([x + 14, y + 10, x + w - 14, y + h - 10], outline=RED, width=6)
    d.line([(x + 22, y + h - 18), (x + w - 22, y + 18)], fill=RED, width=6)


def draw_sudan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 210), outline=INK, width=2)
    # stylised map outline
    d.polygon([(x + 22, y + 14), (x + w - 26, y + 20), (x + w - 18, y + int(h * 0.55)),
               (x + int(w * 0.62), y + h - 14), (x + 26, y + int(h * 0.66)),
               (x + 14, y + int(h * 0.34))], fill=(214, 178, 120), outline=INK)
    # marked region
    d.ellipse([x + int(w * 0.52), y + int(h * 0.34), x + int(w * 0.76), y + int(h * 0.58)],
              fill=RED)
    d.text((x + int(w * 0.55), y + int(h * 0.42)), "BAU", font=font(SANS_B, 16), fill=(255, 255, 255))
    d.text((x + 10, y + 8), "BLUE NILE", font=font(SANS_B, 15), fill=INK)


def draw_bottle(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 228), outline=INK, width=2)
    # bottle
    bx = x + w // 2 - 16
    d.rectangle([bx, y + 14, bx + 32, y + 34], fill=INK)
    d.polygon([(bx, y + 34), (bx + 32, y + 34), (bx + 40, y + 56), (bx - 8, y + 56)],
              fill=(120, 90, 60))
    d.rectangle([bx - 8, y + 56, bx + 40, y + h - 12], fill=(120, 90, 60), outline=INK, width=2)
    d.rectangle([bx + 2, y + 70, bx + 30, y + 92], fill=PAPER)
    d.text((bx + 6, y + 74), "XXX", font=font(SANS_B, 12), fill=RED)
    # warning triangle
    tx, ty = x + int(w * 0.66), y + int(h * 0.62)
    d.polygon([(tx, ty - 18), (tx + 20, ty + 14), (tx - 20, ty + 14)], fill=GOLD, outline=INK)
    d.text((tx - 4, ty - 8), "!", font=font(SANS_B, 18), fill=INK)


def draw_shield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 248), outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2 - 6
    d.polygon([(cx - 42, cy - 34), (cx + 42, cy - 34), (cx + 42, cy + 6),
               (cx, cy + 44), (cx - 42, cy + 6)], fill=BLUE, outline=INK)
    # compass star
    for ang in range(0, 360, 90):
        r = math.radians(ang)
        d.polygon([(cx, cy - 6),
                   (cx + int(7 * math.cos(r - 0.5)), cy + int(7 * math.sin(r - 0.5))),
                   (cx + int(26 * math.cos(r)), cy + int(26 * math.sin(r))),
                   (cx + int(7 * math.cos(r + 0.5)), cy + int(7 * math.sin(r + 0.5)))],
                  fill=(255, 255, 255))
    d.text((x + 8, y + h - 22), "KYIV", font=font(SANS_B, 14), fill=BLUE)


# ---------------------------------------------------------------- page

# (kicker, headline, body, illustration)
PANELS = [
    ("BALTIC DRONE STRIKE",
     "Drones hit Russian ship in Baltic",
     "Finland tightens security; Kyiv blamed for the Gulf of Finland attack.",
     draw_ship),
    ("HONG KONG VOTES",
     "Polls open for 723 seats",
     "856 candidates contest the Election Committee that picks the city's leader.",
     draw_ballot),
    ("MYANMAR SHAKEN",
     "Magnitude 4.1 quake strikes",
     "Early-hours tremor in Myanmar; no casualties reported.",
     draw_quake),
    ("ROBOT WEAPONS FAIL",
     "UN talks end with no rules",
     "Talks on lethal autonomous weapons fail to agree enforceable limits.",
     draw_robot),
    ("SUDAN: BAU FALLS",
     "Tasis Alliance takes Bau",
     "Key Blue Nile region falls as Sudan's war grinds on.",
     draw_sudan),
    ("POISON LIQUOR KILLS 11",
     "Poison liquor kills 11",
     "Illicit alcohol sickens 180 in India's Manipur state.",
     draw_bottle),
    ("ZELENSKYY: NATO IS THE ANSWER",
     "NATO is the answer, says Kyiv",
     "Zelenskyy: membership is the clearest security guarantee.",
     draw_shield),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    right = W - M

    # ---- masthead
    d.text((M, 18), "THE WORLD TODAY", font=font(SERIF_B, 62), fill=INK)
    rule(d, M, 96, right, 4)
    d.text((M, 106), "SUNDAY, 22 NOVEMBER 2026", font=font(SANS_B, 24), fill=RED)
    d.text((right, 110), "ONE DAY  •  ONE PAGE  •  THE WORLD",
           font=font(SANS_B, 15), fill=GREY, anchor="ra")
    rule(d, M, 140, right, 2)

    # ---- headline story
    hy = 156
    art_w, art_h = 400, 262
    ax, ay = right - art_w, hy
    draw_radar_scene(d, ax, ay, art_w, art_h)
    tx = M
    d.text((tx, hy - 4), "MIDDLE EAST  •  LEAD STORY", font=font(SANS_B, 17), fill=RED)
    head = font(SERIF_B, 34)
    y = text_block(d, tx, hy + 26,
                   wrap(d, "Iran claims strikes on US Patriot radars in Bahrain",
                        head, right - art_w - 24 - tx), head, leading=40)
    body = font(SANS, 18)
    y = text_block(d, tx, y + 10,
                   wrap(d, "Tehran says its Revolutionary Guard hit two American air-defence "
                           "radars in the Gulf kingdom, the sharpest escalation yet of the "
                           "regional stand-off.",
                        body, right - art_w - 24 - tx), body, leading=24)
    d.text((tx, ay + art_h - 2), "Bahrain probes reports of a Patriot interceptor crash.",
           font=font(SANS, 14), fill=GREY)
    rule(d, M, 440, right, 2)

    # ---- story grid: row 1 = 4 panels, row 2 = 3 panels
    gap = 12
    gy = 456
    row_h = 246
    col_w4 = (W - 2 * M - 3 * gap) // 4
    col_w3 = (W - 2 * M - 2 * gap) // 3
    for i, (kicker, headline, body_text, art) in enumerate(PANELS):
        if i < 4:
            px = M + i * (col_w4 + gap)
            pw = col_w4
            py = gy
        else:
            j = i - 4
            px = M + j * (col_w3 + gap)
            pw = col_w3
            py = gy + row_h + gap
        ph = row_h
        d.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)
        art(d, px + 8, py + 8, pw - 16, 96)
        kf = font(SANS_B, 14)
        d.text((px + 10, py + 112), kicker, font=kf, fill=RED)
        hf = font(SERIF_B, 18)
        y = text_block(d, px + 10, py + 134,
                       wrap(d, headline, hf, pw - 20), hf, leading=21)
        bf = font(SANS, 14)
        text_block(d, px + 10, y + 3,
                   wrap(d, body_text, bf, pw - 20), bf, leading=18)

    # ---- footer
    fy = gy + 2 * row_h + gap + 12
    rule(d, M, fy, right, 2)
    d.text((M, fy + 8), "THE WORLD TODAY  •  All stories first reported on Sunday 22 November 2026.",
           font=font(SANS, 14), fill=GREY)
    d.text((right, fy + 8), "Page 1 of 1", font=font(SANS, 14), fill=GREY, anchor="ra")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
