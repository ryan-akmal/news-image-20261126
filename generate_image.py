#!/usr/bin/env python3
"""Render the news-image-20261126 front page: 1024x1024 PNG.

Written fresh from the brief. Layout is driven by a small column
engine: every block receives a rectangle and draws inside it.
Deterministic: fixed fonts, fixed geometry, no timestamps, no random.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (22, 22, 20)
ACCENT = (158, 43, 30)
MUTED = (96, 90, 78)
RULE = (60, 56, 48)
HAIR = (178, 172, 156)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FONT_DIR, "liberation/LiberationSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "liberation/LiberationSerif-Regular.ttf")
SANS = os.path.join(FONT_DIR, "liberation/LiberationSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "liberation/LiberationSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.f_title = font(SERIF_B, 62)
        self.f_date = font(SANS_B, 19)
        self.f_kicker = font(SANS_B, 13)
        self.f_lead_head = font(SERIF_B, 42)
        self.f_lead_body = font(SERIF, 20)
        self.f_head = font(SERIF_B, 24)
        self.f_body = font(SANS, 16)
        self.f_strip_head = font(SANS_B, 14)
        self.f_strip = font(SANS, 15)
        self.f_foot = font(SANS, 12)
        self.f_big = font(SERIF_B, 74)

    # -- helpers ---------------------------------------------------------
    def wrap(self, text, f, max_w):
        """Greedy word wrap returning a list of lines."""
        lines, cur = [], ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if self.d.textlength(trial, font=f) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, text, f, max_w, leading, fill=INK):
        for line in self.wrap(text, f, max_w):
            self.d.text((x, y), line, font=f, fill=fill)
            y += leading
        return y

    def hline(self, x0, x1, y, width=1, fill=RULE):
        self.d.line([(x0, y), (x1, y)], fill=fill, width=width)

    def kicker(self, x, y, text):
        self.d.text((x, y), text.upper(), font=self.f_kicker, fill=ACCENT)
        return y + 20

    def letterspaced(self, cx, y, text, f, tracking=4, fill=MUTED):
        total = sum(self.d.textlength(c, font=f) + tracking for c in text) - tracking
        x = cx - total / 2
        for c in text:
            self.d.text((x, y), c, font=f, fill=fill)
            x += self.d.textlength(c, font=f) + tracking

    # -- blocks ----------------------------------------------------------
    def masthead(self, x, y, w):
        title = "THE WORLD IN ONE DAY"
        tw = self.d.textlength(title, font=self.f_title)
        self.d.text((x + (w - tw) / 2, y), title, font=self.f_title, fill=INK)
        self.letterspaced(x + w / 2, y + 78, "THURSDAY  •  26 NOVEMBER 2026",
                          self.f_date)
        self.hline(x, x + w, y + 118, width=3)
        self.hline(x, x + w, y + 124, width=1)
        return y + 136

    def lead(self, x, y, w, h):
        # right-hand figure box
        box_w = 210
        self.d.rectangle([x + w - box_w, y, x + w, y + h], outline=HAIR, width=1)
        self.d.text((x + w - box_w + 18, y + 34), "45%",
                    font=self.f_big, fill=ACCENT)
        self.para(x + w - box_w + 18, y + 122, "top tariff rate on China",
                  self.f_body, box_w - 36, 21, fill=MUTED)
        tx = x
        tw = w - box_w - 28
        yy = self.kicker(tx, y + 8, "Trade war")
        yy = self.para(tx, yy + 2, "US unveils sweeping new tariffs",
                       self.f_lead_head, tw, 48)
        self.para(tx, yy + 6,
                  "Washington proposes Section 301 duties on 14 trading "
                  "partners over factory overcapacity. China is hit hardest, "
                  "at nearly 45%, and markets are rattled.",
                  self.f_lead_body, tw, 27, fill=MUTED)
        self.hline(x, x + w, y + h, width=1, fill=HAIR)
        return y + h

    def panel(self, x, y, w, h, kicker, head, body):
        self.d.rectangle([x, y, x + w, y + h], outline=HAIR, width=1)
        px, py = x + 16, y + 12
        py = self.kicker(px, py, kicker)
        # short accent tick under the kicker
        self.d.line([(px, py - 4), (px + 28, py - 4)], fill=ACCENT, width=2)
        py = self.para(px, py + 4, head, self.f_head, w - 32, 29)
        self.para(px, py + 4, body, self.f_body, w - 32, 21, fill=MUTED)

    def strip(self, x, y, w, h):
        yy = self.kicker(x, y, "Also in the news")
        self.hline(x, x + w, yy + 2, width=1, fill=HAIR)
        items = [
            "BepiColombo reaches Mercury orbit after an 8-year journey",
            "Hera spacecraft revisits asteroid crater 4 years after DART impact",
            "Israeli judge urges dropping the most serious charge against Netanyahu",
            "Pakistani astronaut joins China's Shenzhou-24 mission",
            "Bangladesh raises garment wages by 36%",
            "Colombian police free 20 supermarket hostages",
        ]
        col_w = (w - 28) // 2
        row_h = 40
        for i, item in enumerate(items):
            cx = x + (i % 2) * (col_w + 28)
            cy = yy + 12 + (i // 2) * row_h
            self.d.text((cx, cy), "\u25aa", font=self.f_strip, fill=ACCENT)
            self.para(cx + 16, cy, item, self.f_strip, col_w - 16, 19)
        return y + h

    def footer(self, x, y, w):
        text = "Sources: Reuters  •  KCNA  •  official statements  •  26 November 2026"
        tw = self.d.textlength(text, font=self.f_foot)
        self.d.text((x + (w - tw) / 2, y), text, font=self.f_foot, fill=MUTED)


def build(out_path):
    p = Page()
    mx, mw = 40, W - 80
    y = 30
    y = p.masthead(mx, y, mw)
    y = p.lead(mx, y + 12, mw, 196)
    gy = y + 16
    gw, gh, gut = (mw - 16) // 2, 150, 16
    grid = [
        ("Cairo", "Cairo tanker inferno kills 31",
         "A fuel tanker crashes near the Warraq tunnel in Giza; "
         "31 are killed and 15 injured in the blaze."),
        ("Markets", "Nasdaq sinks nearly 4% in AI rout",
         "US stocks fall again on AI fears; the Nasdaq drops nearly 4% "
         "and Nvidia slides 5%."),
        ("Korea", "Pyongyang expels Swiss envoy",
         "North Korea orders Switzerland to close its diplomatic office "
         "over a sanctions dispute; Kim urges wider tactical nuclear "
         "deployment."),
        ("Ukraine", "Ukraine hits Russian air base",
         "A strike on Savasleyka air base damages five aircraft "
         "(3 MiG-31, 2 Su-34); 88 of 112 drones are shot down overnight."),
    ]
    for i, (kick, head, body) in enumerate(grid):
        px = mx + (i % 2) * (gw + gut)
        py = gy + (i // 2) * (gh + gut)
        p.panel(px, py, gw, gh, kick, head, body)
    by = gy + 2 * gh + gut + 8  # a little air above the bottom panel
    p.panel(mx, by, mw, 104, "The toll",
            "Russia's own toll: nearly 500,000 dead",
            "Moscow's own official data shows nearly half a million "
            "military deaths in the Ukraine war.")
    sy = by + 104 + 16
    p.strip(mx, sy, mw, 132)
    p.footer(mx, H - 26, mw)
    p.img.save(out_path, format="PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
