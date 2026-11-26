#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Every pictogram is original flat Pillow artwork, every word is set in
DejaVu. No photograph, no borrowed art, no network access. Deterministic:
same input, same bytes.
Run:  python3 generate_image.py   (writes entry.png here)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 245, 236)
INK = (22, 30, 46)
NAVY = (14, 28, 56)
GOLD = (232, 194, 104)
RED = (176, 32, 32)
MUTED = (96, 96, 96)
GREY = (62, 62, 62)
EDGE = (204, 198, 188)
STRIP = (232, 226, 212)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, face, width):
    rows, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=face) <= width:
            cur = trial
        else:
            if cur:
                rows.append(cur)
            cur = word
    if cur:
        rows.append(cur)
    return rows


def block(d, x, y, text, face, colour, width, step):
    for line in wrap(d, text, face, width):
        d.text((x, y), line, font=face, fill=colour)
        y += step
    return y


def flame(d, cx, base, w, h):
    d.polygon([(cx - w, base), (cx - w * 0.5, base - h * 0.5),
               (cx - w * 0.12, base - h * 0.78), (cx + w * 0.22, base - h),
               (cx + w * 0.5, base - h * 0.5), (cx + w, base - h * 0.28),
               (cx + w * 0.42, base)], fill=(228, 122, 30))
    d.polygon([(cx - w * 0.42, base), (cx - w * 0.12, base - h * 0.42),
               (cx + w * 0.18, base - h * 0.52), (cx + w * 0.42, base)],
              fill=(247, 202, 72))


def puff(d, cx, cy, r, colour=(170, 170, 170)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)


def burst(d, cx, cy, r_out, r_in, points, colour):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=colour)


# ---------- pictograms, drawn inside a square of side s ----------
def pic_ship(d, x, y, s):
    # Container ship with stacked boxes and a % badge.
    hull = y + s * 0.62
    d.polygon([(x + s * 0.04, hull), (x + s * 0.96, hull),
               (x + s * 0.88, y + s * 0.84), (x + s * 0.12, y + s * 0.84)],
              fill=(48, 66, 94), outline=NAVY, width=3)
    for i, col in enumerate(((232, 194, 104), (70, 130, 160), (178, 80, 60))):
        bx = x + s * (0.14 + i * 0.22)
        d.rectangle([bx, y + s * 0.34, bx + s * 0.20, hull],
                    fill=col, outline=NAVY, width=2)
        d.rectangle([bx, y + s * 0.20, bx + s * 0.20, y + s * 0.32],
                    fill=col, outline=NAVY, width=2)
    d.rectangle([x + s * 0.80, y + s * 0.30, x + s * 0.94, hull],
                fill=(210, 210, 205), outline=NAVY, width=2)
    d.ellipse([x + s * 0.06, y + s * 0.06, x + s * 0.30, y + s * 0.30],
              fill=(176, 32, 32), outline=NAVY, width=2)
    d.text((x + s * 0.18, y + s * 0.07), "%", font=f(BOLD, 22),
           fill=(255, 255, 255), anchor="ma")


def pic_truck(d, x, y, s):
    # Fuel tanker truck with flames and smoke.
    d.rounded_rectangle([x + s * 0.08, y + s * 0.42, x + s * 0.62, y + s * 0.72],
                        radius=12, fill=(150, 158, 172), outline=NAVY, width=3)
    d.rectangle([x + s * 0.62, y + s * 0.46, x + s * 0.86, y + s * 0.72],
                fill=(178, 80, 60), outline=NAVY, width=3)
    d.ellipse([x + s * 0.20, y + s * 0.72, x + s * 0.34, y + s * 0.86],
              fill=(30, 30, 30))
    d.ellipse([x + s * 0.68, y + s * 0.72, x + s * 0.82, y + s * 0.86],
              fill=(30, 30, 30))
    flame(d, x + s * 0.30, y + s * 0.44, 22, 40)
    flame(d, x + s * 0.52, y + s * 0.44, 18, 32)
    puff(d, x + s * 0.78, y + s * 0.14, 12)
    puff(d, x + s * 0.66, y + s * 0.08, 9, (190, 190, 190))


def pic_chart(d, x, y, s):
    # Axes and a steep falling line with a down arrow.
    d.line([(x + s * 0.12, y + s * 0.08), (x + s * 0.12, y + s * 0.88)],
           fill=INK, width=4)
    d.line([(x + s * 0.12, y + s * 0.88), (x + s * 0.92, y + s * 0.88)],
           fill=INK, width=4)
    pts = [(x + s * 0.20, y + s * 0.28), (x + s * 0.38, y + s * 0.34),
           (x + s * 0.56, y + s * 0.46), (x + s * 0.74, y + s * 0.64),
           (x + s * 0.86, y + s * 0.78)]
    d.line(pts, fill=RED, width=6, joint="curve")
    d.polygon([(pts[-1][0] - 2, pts[-1][1] + 15), (pts[-1][0] - 15, pts[-1][1] - 7),
               (pts[-1][0] + 13, pts[-1][1] - 7)], fill=RED)
    for px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED)


def pic_embassy(d, x, y, s):
    # A government building with a flag and a closed gate.
    d.rectangle([x + s * 0.16, y + s * 0.40, x + s * 0.84, y + s * 0.92],
                fill=(120, 128, 146), outline=NAVY, width=3)
    d.polygon([(x + s * 0.08, y + s * 0.40), (x + s * 0.50, y + s * 0.18),
               (x + s * 0.92, y + s * 0.40)], fill=(70, 80, 100),
              outline=NAVY, width=3)
    d.rectangle([x + s * 0.44, y + s * 0.62, x + s * 0.56, y + s * 0.92],
                fill=(40, 44, 60))
    for wy in (y + s * 0.50, y + s * 0.68):
        d.rectangle([x + s * 0.24, wy, x + s * 0.34, wy + 10], fill=(232, 194, 104))
        d.rectangle([x + s * 0.66, wy, x + s * 0.76, wy + 10], fill=(232, 194, 104))
    d.line([(x + s * 0.50, y + s * 0.18), (x + s * 0.50, y + s * 0.04)],
           fill=NAVY, width=3)
    d.polygon([(x + s * 0.50, y + s * 0.04), (x + s * 0.78, y + s * 0.10),
               (x + s * 0.50, y + s * 0.16)], fill=RED)


def pic_jet(d, x, y, s):
    # A fighter jet in profile over a runway stripe.
    d.polygon([(x + s * 0.06, y + s * 0.52), (x + s * 0.55, y + s * 0.38),
               (x + s * 0.94, y + s * 0.30), (x + s * 0.88, y + s * 0.46),
               (x + s * 0.60, y + s * 0.56), (x + s * 0.52, y + s * 0.66),
               (x + s * 0.40, y + s * 0.58), (x + s * 0.30, y + s * 0.66),
               (x + s * 0.22, y + s * 0.58)],
              fill=(70, 82, 104), outline=NAVY, width=3)
    d.ellipse([x + s * 0.62, y + s * 0.36, x + s * 0.76, y + s * 0.46],
              fill=(232, 194, 104))
    burst(d, x + s * 0.08, y + s * 0.24, 14, 6, 6, (255, 214, 110))
    d.rectangle([x + s * 0.06, y + s * 0.86, x + s * 0.94, y + s * 0.92],
                fill=(64, 64, 64))
    for wx in (0.16, 0.40, 0.64, 0.84):
        d.rectangle([x + s * wx, y + s * 0.86, x + s * (wx + 0.08), y + s * 0.92],
                    fill=(232, 194, 104))


def pic_memorial(d, x, y, s):
    # Three plain crosses on a low hill.
    d.ellipse([x + s * 0.06, y + s * 0.78, x + s * 0.94, y + s * 0.96],
              fill=(120, 128, 110))
    for cx, hgt in ((0.22, 0.42), (0.50, 0.56), (0.78, 0.42)):
        cxp = x + s * cx
        top = y + s * (0.80 - hgt)
        d.rectangle([cxp - 4, top, cxp + 4, y + s * 0.80], fill=(52, 52, 52))
        d.rectangle([cxp - 14, top + 10, cxp + 14, top + 18], fill=(52, 52, 52))


PANELS = [
    # (tag, accent, headline, caption, pictogram)
    ("EGYPT", (120, 40, 32), "CAIRO TANKER INFERNO KILLS 31",
     "A fuel tanker crashes on the highway near the Warraq tunnel in "
     "Giza; a huge fire follows, 31 killed, 15 injured.", pic_truck),
    ("MARKETS", (155, 34, 38), "NASDAQ SINKS NEARLY 4% IN AI ROUT",
     "US stocks fall further as AI fears intensify; Nvidia down 5% and "
     "all three main indexes slide.", pic_chart),
    ("NORTH KOREA", (40, 70, 110), "PYONGYANG EXPELS SWISS ENVOY",
     "North Korea orders Switzerland to close its diplomatic office in a "
     "sanctions row; Kim urges wider nuclear deployment.", pic_embassy),
    ("UKRAINE", (42, 110, 143), "UKRAINE HITS RUSSIAN AIR BASE",
     "A strike on Savasleyka airbase damages five planes \u2014 three "
     "MiG-31s and two Su-34s; 88 of 112 drones downed.", pic_jet),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD IN ONE DAY",
           font=f(SERIF, 54), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 80), "THURSDAY  \u2022  26 NOVEMBER 2026",
           font=f(BOLD, 30), fill=GOLD, anchor="ma")
    d.rectangle([0, 128, W, 134], fill=GOLD)

    # Standfirst
    block(d, 28, 146,
          "Six stories that defined the day: new US tariffs, a tanker "
          "inferno outside Cairo, Nasdaq's AI rout, a Swiss envoy expelled, "
          "a Russian air base hit \u2014 and Moscow's own war toll.",
          f(PLAIN, 19), INK, W - 56, 25)

    # Lead story, full width
    lx, ly, lw, lh = 24, 206, W - 48, 156
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=(255, 255, 255),
                outline=EDGE, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 30], fill=(28, 60, 110))
    d.text((lx + 14, ly + 3), "TRADE  \u2022  WASHINGTON",
           font=f(BOLD, 18), fill=(255, 255, 255))
    pic_ship(d, lx + lw - 168, ly + 38, 124)
    block(d, lx + 16, ly + 42, "US UNVEILS SWEEPING NEW TARIFFS",
          f(BOLD, 31), INK, lw - 200, 38)
    block(d, lx + 16, ly + 90,
          "Washington proposes Section 301 duties on 14 trading partners "
          "to fight factory overcapacity; China is hit hardest, at nearly "
          "45%, and markets recoil.",
          f(PLAIN, 18), GREY, lw - 200, 24)

    # Four panels: 2 columns x 2 rows
    gx, gy = 24, 378
    pw, ph, gap = 480, 176, 16
    for i, (tag, accent, head, cap, pic) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(255, 255, 255),
                    outline=EDGE, width=2)
        d.rectangle([x0, y0, x0 + pw, y0 + 30], fill=accent)
        d.text((x0 + 14, y0 + 3), tag, font=f(BOLD, 18),
               fill=(255, 255, 255))
        pic(d, x0 + 10, y0 + 40, 118)
        block(d, x0 + 140, y0 + 42, head, f(BOLD, 24), INK,
              pw - 156, 29)
        block(d, x0 + 140, y0 + 106, cap, f(PLAIN, 16),
              GREY, pw - 156, 21)

    # Bottom panel, full width: the war toll
    sx, sy, sw, sh = 24, 762, W - 48, 84
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=(255, 255, 255),
                outline=EDGE, width=2)
    d.rectangle([sx, sy, sx + 150, sy + sh], fill=(70, 70, 70))
    d.text((sx + 75, sy + 26), "THE TOLL", font=f(BOLD, 22),
           fill=(255, 255, 255), anchor="ma")
    pic_memorial(d, sx + 158, sy + 6, 66)
    block(d, sx + 232, sy + 10, "RUSSIA'S OWN TOLL: NEARLY 500,000 DEAD",
          f(BOLD, 25), INK, sw - 250, 31)
    block(d, sx + 232, sy + 44,
          "Moscow's own figures show almost half a million military deaths "
          "in the Ukraine war.",
          f(PLAIN, 16), GREY, sw - 250, 21)

    # Also in the news
    ay = 856
    d.rectangle([24, ay, W - 24, ay + 88], fill=STRIP,
                outline=EDGE, width=2)
    block(d, 40, ay + 8,
          "ALSO IN THE NEWS:  BepiColombo reaches Mercury orbit after 8 "
          "years  \u2022  Hera probe revisits the asteroid crater  \u2022  "
          "Israeli judges urge dropping gravest Netanyahu charges  \u2022  "
          "Pakistani astronaut joins Shenzhou-24  \u2022  Bangladesh raises "
          "garment wages 36%  \u2022  Colombia frees 20 supermarket "
          "hostages",
          f(BOLD, 15), INK, W - 80, 20)

    # Footer
    d.text((W // 2, H - 26),
           "Sources: Reuters, BBC, AP, EUR Radio \u2014 "
           "reported 26 November 2026",
           font=f(PLAIN, 15), fill=MUTED, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
