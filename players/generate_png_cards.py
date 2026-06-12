"""
Generates 1080x1920 PNG player cards for YouTube Shorts.
Uses Pillow. Run locally after placing real photos in players/images/
to regenerate with actual faces.
"""

import json
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

IMAGES_DIR  = os.path.join(os.path.dirname(__file__), "images")
CARDS_DIR   = os.path.join(os.path.dirname(__file__), "cards")
METADATA    = os.path.join(os.path.dirname(__file__), "metadata.json")

W, H = 1080, 1920

# Country primary/secondary jersey colours
THEMES = {
    "Argentina": dict(c1=(116, 172, 223), c2=(255, 255, 255), text=(255, 255, 255), accent=(255, 255, 255)),
    "Portugal":  dict(c1=(0,  100,  0  ), c2=(196, 0, 0     ), text=(255, 255, 255), accent=(255, 215, 0)),
    "France":    dict(c1=(0,   35, 149  ), c2=(237, 41,  57  ), text=(255, 255, 255), accent=(255, 255, 255)),
    "Brazil":    dict(c1=(0,  156,  59  ), c2=(255, 223, 0   ), text=(255, 255, 255), accent=(255, 223, 0)),
    "Norway":    dict(c1=(239, 43,  45  ), c2=(255, 255, 255  ), text=(255, 255, 255), accent=(0, 50, 160)),
    "England":   dict(c1=(200, 200, 220 ), c2=(207,   8,  31  ), text=(20,  20,  50 ), accent=(207, 8, 31)),
    "Spain":     dict(c1=(170, 21,  27  ), c2=(241, 191,   0  ), text=(255, 255, 255), accent=(241, 191, 0)),
    "Germany":   dict(c1=(20,  20,  20  ), c2=(221,   0,   0  ), text=(255, 255, 255), accent=(255, 206, 0)),
}


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_gradient(draw, c1, c2, w, h):
    for y in range(h):
        t = y / h
        # subtle diagonal + top-heavy fade
        col = lerp_color(c1, c2, t * 0.65)
        draw.line([(0, y), (w, y)], fill=col)


def draw_diagonal_stripe(img, c2, alpha=40):
    """Subtle diagonal stripe overlay for texture."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    stripe_w = 120
    for x in range(-H, W + H, stripe_w * 2):
        pts = [(x, 0), (x + stripe_w, 0), (x + stripe_w + H, H), (x + H, H)]
        od.polygon(pts, fill=(*c2, alpha))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"),
              (0, 0))


def get_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines, line = [], []
    for word in words:
        test = " ".join(line + [word])
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] <= max_width or not line:
            line.append(word)
        else:
            lines.append(" ".join(line))
            line = [word]
    if line:
        lines.append(" ".join(line))
    return lines


def make_card(player, theme):
    c1, c2 = theme["c1"], theme["c2"]
    text_c = theme["text"]
    accent = theme["accent"]

    img = Image.new("RGB", (W, H), c1)
    draw = ImageDraw.Draw(img)

    # ── background gradient ──────────────────────────────
    draw_gradient(draw, c1, c2, W, H)
    draw_diagonal_stripe(img, c2, alpha=30)
    draw = ImageDraw.Draw(img)          # re-acquire after paste

    # ── big circular "badge" area ────────────────────────
    cx, cy, r = W // 2, 760, 340
    # dark semi-circle for depth
    draw.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10],
                 fill=(*[max(0, v - 40) for v in c1],))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c1)

    # Jersey number silhouette — big "?" or jersey icon
    font_big = get_font(320)
    draw.text((cx, cy), "?", font=font_big, fill=(*c2, ), anchor="mm")

    # ── top bar ──────────────────────────────────────────
    bar_h = 160
    draw.rectangle([0, 0, W, bar_h], fill=tuple(max(0, v - 20) for v in c1))
    draw.rectangle([0, bar_h - 6, W, bar_h], fill=accent)

    # Country name (top-right)
    font_country = get_font(68, bold=True)
    draw.text((W - 50, bar_h // 2), player["country"].upper(),
              font=font_country, fill=text_c, anchor="rm")

    # ── bottom name plate ────────────────────────────────
    plate_y = H - 320
    draw.rectangle([0, plate_y, W, H], fill=tuple(max(0, v - 30) for v in c1))
    draw.rectangle([0, plate_y, W, plate_y + 8], fill=accent)

    # Player name — may wrap for long names
    font_name = get_font(100, bold=True)
    name_lines = wrap_text(player["name"].upper(), font_name, W - 80, draw)
    total_h = len(name_lines) * 110
    start_y = plate_y + (H - plate_y - total_h) // 2
    for i, line in enumerate(name_lines):
        draw.text((W // 2, start_y + i * 110), line,
                  font=font_name, fill=text_c, anchor="mm")

    # Optional note (e.g. "back after 2 years out")
    if player.get("note"):
        font_note = get_font(46)
        draw.text((W // 2, H - 50), player["note"],
                  font=font_note, fill=accent, anchor="mb")

    # ── accent dots (decorative) ─────────────────────────
    for i in range(5):
        dot_x = 60 + i * 60
        draw.ellipse([dot_x - 8, H - 280 - 8, dot_x + 8, H - 280 + 8],
                     fill=accent)

    return img


def main():
    os.makedirs(CARDS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    with open(METADATA) as f:
        players = json.load(f)

    for player in players:
        theme = THEMES.get(player["country"],
                           dict(c1=(30,30,30), c2=(80,80,80), text=(255,255,255), accent=(255,255,0)))

        real_photo = os.path.join(IMAGES_DIR, player["image_file"])
        slug = os.path.splitext(player["image_file"])[0]
        out_path = os.path.join(CARDS_DIR, f"{slug}.png")

        if os.path.exists(real_photo):
            # Composite real photo over the gradient card
            card = make_card(player, theme)
            photo = Image.open(real_photo).convert("RGB")
            # Fit photo into the badge circle area
            photo = photo.resize((680, 900), Image.LANCZOS)
            card.paste(photo, ((W - 680) // 2, 200))
        else:
            card = make_card(player, theme)

        card.save(out_path, "PNG", optimize=True)
        kb = os.path.getsize(out_path) // 1024
        status = "photo" if os.path.exists(real_photo) else "placeholder"
        print(f"  [{status}] {player['name']} → cards/{slug}.png  ({kb} KB)")

    print(f"\n{len(players)} PNG cards saved to players/cards/")


if __name__ == "__main__":
    main()
