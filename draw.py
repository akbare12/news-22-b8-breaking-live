#!/usr/bin/env python3
"""NEWS-22 B8 — LIVE BLOG: the day as a reverse-chronological live-updates feed.
Draws entry.png (1024x1024) with PIL only. Deterministic: no timestamps, no randomness.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (26, 26, 26)
NAVY = (22, 38, 74)
RED = (179, 32, 44)
RED_DK = (140, 20, 30)
GREEN = (46, 125, 50)
AMBER = (180, 83, 9)
BLUE = (29, 78, 216)
MUTED = (90, 90, 82)
LINE = (200, 192, 172)
MAP_BG = (214, 228, 235)
MAP_LAND = (226, 205, 160)

FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_MAST = font("DejaVuSerif-Bold.ttf", 46)
F_SERIF_B = font("DejaVuSerif-Bold.ttf", 20)
F_SANS_B = font("DejaVuSans-Bold.ttf", 13)
F_SANS = font("DejaVuSans.ttf", 12)
F_SMALL = font("DejaVuSans.ttf", 10)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 10)
F_TINY = font("DejaVuSans.ttf", 9)
F_TINY_B = font("DejaVuSans-Bold.ttf", 9)
F_TIME = font("DejaVuSansMono-Bold.ttf", 12)
F_TIME_BIG = font("DejaVuSansMono-Bold.ttf", 15)
F_NUM = font("DejaVuSans-Bold.ttf", 22)
F_NUM_LBL = font("DejaVuSans.ttf", 10)
F_HERO_H = font("DejaVuSerif-Bold.ttf", 24)
F_HERO_B = font("DejaVuSans.ttf", 11)
F_HERO_S = font("DejaVuSans-Bold.ttf", 9)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def trunc(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."

def badge(draw, x, y, text, fg, bg, fnt=F_TINY_B, pad_x=5, pad_y=2):
    w = draw.textlength(text, font=fnt) + pad_x * 2
    h = fnt.size + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fg)
    return w

# ---------------------------------------------------------------- feed data
# (time, headline, detail, source, status)  status: R=REPORTED, C=CLAIM
FEED = [
    ("15:36", "Merkury hit at Benghazi", "Ukraine: 7 naval drones sank Russian corvette at Libyan port.", "France 24", "C"),
    ("15:03", "Khartoum drones kill 4", "UN building damaged; strikes blamed on Sudan's RSF.", "AP", "C"),
    ("14:48", "Zelenskyy pleads Patriots", "Russia fired ~2,700 drones in a week; Dymer flats hit.", "BBC", "R"),
    ("14:20", "Iran shows missile city", "Dual-missile launcher unveiled in underground tunnels.", "IRGC media", "R"),
    ("13:16", "Saudis stop Houthi attack", "Drone + missile intercepted; Rabigh refinery claimed hit.", "Reuters", "C"),
    ("12:00", "COP31 ends, no deal", "EU + ~130 parties reject text with no fossil fuels.", "CNN · Reuters", "R"),
    ("10:25", "Ex-police chief found dead", "Amid Sicily bombing cover-up inquiry; Meloni shocked.", "ANSA", "R"),
    ("09:53", "UAE condemns Bahrain strike", "Calls Iran attack a flagrant sovereignty violation.", "WAM", "R"),
    ("09:41", "Europe protests, day 3", "Cost & housing marches; 6th weekend in a row in France.", "AP", "R"),
    ("07:47", "Settlers burn 12 cars", "West Bank villages attacked; racist graffiti on homes.", "WAFA", "R"),
    ("07:36", "Benghazi depot blast", "Ammo depot fire inside naval base; cause unknown.", "Local auth.", "R"),
    ("06:58", "Unity talks stall", "Eisenkot-Likud meet; wide gap on unity government.", "Israeli media", "R"),
    ("06:15", "Finland: war spills over", "Drone hits Russian cargo ship in the Baltic Sea.", "Finnish govt", "R"),
    ("05:48", "WCK: 3 killed not its team", "Gaza aid-van victims were not World Central Kitchen.", "WCK", "R"),
    ("04:22", "Ex-UN envoy: war avoidable", "De Soto: the Iran war need not have happened.", "MED Dialogues", "R"),
    ("04:19", "Banten factory fire", "3 dead, 36 missing in Cikande candy factory blaze.", "BBC", "R"),
    ("03:56", "Fidan: Israel may use Druze", "To provoke a Syrian army operation, Turkey warns.", "Anadolu", "C"),
    ("03:24", "Bahrain blames Iran", "Industrial site hit Saturday; no casualties reported.", "France 24", "R"),
    ("03:18", "Fidan: war fallout hits markets", "US-Israel war burden threatens global markets.", "Anadolu", "R"),
    ("02:38", "Aoun: Israel must leave", "'Every inch' of Lebanon, president demands.", "Al Jazeera", "R"),
    ("02:14", "Gaza: 350,000 homeless", "Protest near Yellow Line as strikes continue.", "Al Jazeera", "R"),
    ("02:09", "Pezeshkian: 'silent war'", "Iran in silent economic war; blockade hits 130 days.", "IRNA", "R"),
    ("01:35", "Settlers attack homes", "Hebron & Ramallah; tear gas fired in raid.", "WAFA", "R"),
    ("01:04", "Turkey: Gaza homes blocked", "Israel blocking thousands of container homes.", "Anadolu", "C"),
    ("00:44", "Hind Rajab urges arrest", "Germany asked to arrest Israeli soldier in Luneburg.", "HRF", "R"),
    ("00:26", "Fred Nile dies at 92", "NSW Christian Democratic figurehead passes away.", "Guardian", "R"),
    ("00:09", "Gamer rescues missing girl", "Teen, 16, and his mother help FBI free runaway.", "FBI", "R"),
    ("00:04", "Gaza toll 1,661", "Since Oct 2025 ceasefire; 6,062 wounded.", "Gaza health min.", "R"),
]

NUMBERS = [
    ("258", "House seats"),
    ("2", "tankers hit"),
    ("194", "COP31 parties"),
    ("330", "votes in NC"),
    ("36", "missing Banten"),
    ("1,661", "Gaza toll"),
]

# pin: (label, dot x frac, dot y frac, label x frac, label y frac)
PINS = [
    ("1 Hormuz", 0.615, 0.52, 0.74, 0.78),
    ("2 Antalya", 0.565, 0.36, 0.64, 0.08),
    ("3 Washington", 0.185, 0.34, 0.10, 0.58),
    ("4 Benghazi", 0.545, 0.47, 0.42, 0.78),
    ("5 Khartoum", 0.575, 0.60, 0.62, 0.92),
    ("6 Kyiv", 0.555, 0.26, 0.47, 0.06),
    ("7 Banten", 0.815, 0.66, 0.88, 0.48),
    ("8 Gaza", 0.585, 0.44, 0.70, 0.32),
]

def draw_map(draw, x0, y0, mw, mh):
    draw.rectangle([x0, y0, x0 + mw, y0 + mh], fill=MAP_BG, outline=LINE)
    # rough continents (fractions of map box)
    def poly(pts, fill=MAP_LAND):
        draw.polygon([(x0 + fx * mw, y0 + fy * mh) for fx, fy in pts], fill=fill)
    # North America
    poly([(0.03, 0.30), (0.10, 0.14), (0.22, 0.12), (0.28, 0.22), (0.24, 0.38),
          (0.16, 0.52), (0.12, 0.62), (0.08, 0.48), (0.03, 0.42)])
    # Greenland
    poly([(0.30, 0.08), (0.35, 0.07), (0.36, 0.14), (0.31, 0.15)])
    # South America
    poly([(0.20, 0.58), (0.27, 0.56), (0.31, 0.66), (0.28, 0.82), (0.23, 0.88),
          (0.20, 0.74)])
    # Europe + Africa + Asia (one Eurasian mass, simplified)
    poly([(0.44, 0.16), (0.52, 0.10), (0.66, 0.08), (0.86, 0.12), (0.97, 0.22),
          (0.93, 0.34), (0.84, 0.40), (0.78, 0.52), (0.70, 0.46), (0.66, 0.58),
          (0.60, 0.72), (0.56, 0.62), (0.52, 0.52), (0.46, 0.44), (0.44, 0.30)])
    # Australia
    poly([(0.82, 0.66), (0.90, 0.64), (0.94, 0.72), (0.88, 0.78), (0.82, 0.74)])
    # UK + Japan dots
    draw.ellipse([x0 + 0.455 * mw - 2, y0 + 0.20 * mh - 2, x0 + 0.455 * mw + 2, y0 + 0.20 * mh + 2], fill=MAP_LAND)
    draw.ellipse([x0 + 0.935 * mw - 2, y0 + 0.30 * mh - 2, x0 + 0.935 * mw + 2, y0 + 0.30 * mh + 2], fill=MAP_LAND)
    for i, (label, fx, fy, lx, ly) in enumerate(PINS, start=1):
        px, py = x0 + fx * mw, y0 + fy * mh
        cx, cy = x0 + lx * mw, y0 + ly * mh
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        draw.line([px, py, cx, cy], fill=RED, width=1)
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255))
        draw.text((cx - 3, cy - 5), str(i), font=F_TINY_B, fill=(255, 255, 255))

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 16  # margin

    # ---- masthead ----
    d.text((MX, 6), "THE WORLD TODAY", font=F_MAST, fill=INK)
    d.text((MX, 56), "LIVE BLOG  ·  SUNDAY 22 NOVEMBER 2026  ·  30 STORIES  ·  ALL TIMES UTC",
           font=F_SMALL_B, fill=MUTED)
    # LIVE badge top-right
    bw = d.textlength("● LIVE", font=F_SANS_B) + 16
    d.rounded_rectangle([W - MX - bw, 14, W - MX, 14 + 30], radius=4, fill=RED)
    d.text((W - MX - bw + 8, 20), "● LIVE", font=F_SANS_B, fill=(255, 255, 255))
    d.line([MX, 76, W - MX, 76], fill=RED, width=3)

    # ---- live bar ----
    y = 82
    d.rectangle([MX, y, W - MX, y + 26], fill=NAVY)
    d.text((MX + 10, y + 6), "LIVE BLOG — THE DAY AS IT HAPPENED, NEWEST FIRST",
           font=F_SMALL_B, fill=(255, 255, 255))
    d.text((W - MX - 10 - d.textlength("UPDATED 23:45 UTC", font=F_SMALL_B), y + 6),
           "UPDATED 23:45 UTC", font=F_SMALL_B, fill=(255, 220, 120))

    # ---- numbers strip ----
    y = 114
    d.rectangle([MX, y, W - MX, y + 40], fill=(255, 255, 255), outline=LINE)
    seg_w = (W - 2 * MX) / len(NUMBERS)
    for i, (num, lbl) in enumerate(NUMBERS):
        cx = MX + seg_w * i + seg_w / 2
        nw = d.textlength(num, font=F_NUM)
        lw = d.textlength(lbl, font=F_NUM_LBL)
        total = nw + 5 + lw
        x0 = cx - total / 2
        d.text((x0, y + 8), num, font=F_NUM, fill=RED)
        d.text((x0 + nw + 5, y + 15), lbl, font=F_NUM_LBL, fill=INK)
        if i:
            d.line([MX + seg_w * i, y + 8, MX + seg_w * i, y + 32], fill=LINE, width=1)

    # ---- hero row: 2 story cards + map panel ----
    y = 160
    HH = 140
    col_w = (W - 2 * MX - 16) / 3
    # hero 1: Dems 258
    x = MX
    d.rectangle([x, y, x + col_w, y + HH], fill=(255, 255, 255), outline=LINE)
    d.rectangle([x, y, x + col_w, y + 22], fill=NAVY)
    d.text((x + 8, y + 4), "18:00 UTC  ·  TOP UPDATE", font=F_TINY_B, fill=(255, 255, 255))
    d.text((x + 8, y + 28), "DEMS WIN 258", font=F_HERO_H, fill=NAVY)
    body = wrap(d, "Hubbard beats Foxx by 330 votes in the NC recount — the largest Dem House majority since 1992. GOP 173; 4 races uncalled.", F_HERO_B, col_w - 16)
    yy = y + 58
    for ln in body[:3]:
        d.text((x + 8, yy), ln, font=F_HERO_B, fill=INK)
        yy += 14
    d.text((x + 8, y + HH - 16), "REPORTED  ·  AP · Reuters", font=F_HERO_S, fill=GREEN)
    # hero 2: Hormuz
    x = MX + col_w + 8
    d.rectangle([x, y, x + col_w, y + HH], fill=(255, 255, 255), outline=LINE)
    d.rectangle([x, y, x + col_w, y + 22], fill=RED)
    d.text((x + 8, y + 4), "17:13 UTC  ·  BREAKING", font=F_TINY_B, fill=(255, 255, 255))
    d.text((x + 8, y + 28), "2 TANKERS HIT", font=F_HERO_H, fill=RED_DK)
    body = wrap(d, "Two supertankers hit mines east of the Strait of Hormuz, north of Ghanam Island; both on fire. Iran navy warns of heavy losses.", F_HERO_B, col_w - 16)
    yy = y + 58
    for ln in body[:3]:
        d.text((x + 8, yy), ln, font=F_HERO_B, fill=INK)
        yy += 14
    d.text((x + 8, y + HH - 16), "REPORTED  ·  Iran navy · AP", font=F_HERO_S, fill=GREEN)
    # hero 3: map panel
    x = MX + 2 * (col_w + 8)
    d.rectangle([x, y, x + col_w, y + HH], fill=(255, 255, 255), outline=LINE)
    d.rectangle([x, y, x + col_w, y + 22], fill=NAVY)
    d.text((x + 8, y + 4), "WHERE IT HAPPENED", font=F_TINY_B, fill=(255, 255, 255))
    draw_map(d, x + 6, y + 27, col_w - 12, 70)
    key = "1 Hormuz · 2 Antalya · 3 Washington · 4 Benghazi"
    key2 = "5 Khartoum · 6 Kyiv · 7 Banten · 8 Gaza"
    d.text((x + 8, y + 102), key, font=F_TINY, fill=INK)
    d.text((x + 8, y + 116), key2, font=F_TINY, fill=INK)

    # ---- feed header ----
    y = 308
    d.text((MX, y), "LIVE FEED — NEWEST FIRST", font=F_SANS_B, fill=INK)
    lx = W - MX
    for txt, bg in [("ONGOING", BLUE), ("CLAIM", AMBER), ("REPORTED", GREEN)]:
        w = d.textlength(txt, font=F_TINY_B) + 10
        lx -= w
        badge(d, lx, y - 1, txt, (255, 255, 255), bg)
        lx -= 6
    d.line([MX, y + 20, W - MX, y + 20], fill=INK, width=1)

    # ---- feed: 2 columns x 14 rows ----
    y0 = 336
    row_h = 41
    col_gap = 12
    cw = (W - 2 * MX - col_gap) / 2
    for idx, (tm, head, det, src, st) in enumerate(FEED):
        col = idx % 2
        row = idx // 2
        ex = MX + col * (cw + col_gap)
        ey = y0 + row * row_h
        if idx == 5:  # COP31 highlight
            d.rectangle([ex - 4, ey - 3, ex + cw + 4, ey + row_h - 6], fill=(255, 243, 224), outline=(230, 190, 120))
        # time badge
        d.text((ex, ey), tm, font=F_TIME, fill=RED)
        hx = ex + 52
        # headline (truncate to fit, leaving room for CLAIM badge)
        head_w = cw - 52 - (44 if st == "C" else 0)
        htxt = trunc(d, head, F_SANS_B, head_w)
        d.text((hx, ey), htxt, font=F_SANS_B, fill=INK)
        if st == "C":
            badge(d, ex + cw - 40, ey, "CLAIM", (255, 255, 255), AMBER)
        # detail line
        det_txt = trunc(d, det + " — " + src, F_SMALL, cw - 52)
        d.text((hx, ey + 17), det_txt, font=F_SMALL, fill=MUTED)
        d.line([ex, ey + row_h - 8, ex + cw, ey + row_h - 8], fill=(228, 222, 206), width=1)

    # ---- NOT YET strip ----
    y = 916
    d.rectangle([MX, y, W - MX, y + 24], fill=(255, 243, 205), outline=(210, 180, 90))
    d.text((MX + 8, y + 5),
           "NOT YET — DO NOT READ AS DONE:  4 House races uncalled  ·  COP32 venue not set  ·  Gaza ceasefire talks: no deal announced",
           font=F_SMALL_B, fill=(120, 80, 0))

    # ---- date check ----
    y = 946
    d.text((MX, y), "DATE CHECK — Every story above was first reported on 22 Nov, unless its kicker says otherwise.  EXCLUDED:",
           font=F_TINY_B, fill=INK)
    d.text((MX, y + 13),
           "El Chapo Isidro captured 20 Nov  ·  BepiColombo Mercury orbit 21 Nov  ·  ICJ Myanmar ruling 19 Nov  ·  Wall St rout 20 Nov  ·  FBI NCIC hack first reported 21 Nov.",
           font=F_TINY, fill=MUTED)
    # ---- legend + sources ----
    y = 976
    d.text((MX, y), "LEGEND:  REPORTED = confirmed by 2+ sources  ·  CLAIM = one side alleges, unverified  ·  ONGOING = still developing.",
           font=F_TINY, fill=MUTED)
    d.text((MX, y + 13),
           "SOURCES: AP · Reuters · BBC · CNN · France 24 · Al Jazeera · Guardian · SCMP · IRNA · Anadolu · WAFA · HRF · WCK · CNBC · The Hindu",
           font=F_TINY, fill=MUTED)
    d.text((MX, y + 26), "THE WORLD TODAY  ·  22 NOV 2026", font=F_TINY_B, fill=MUTED)

    out = os.environ.get("OUT", "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
