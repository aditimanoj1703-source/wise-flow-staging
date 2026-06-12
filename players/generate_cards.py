"""
Generates SVG player cards for YouTube Shorts preview.
Each card shows the player photo (if downloaded) or a flag-coloured placeholder,
plus the player name, country, and flag emoji.

Usage:
    python3 players/generate_cards.py
Output: players/cards/*.svg
"""

import json
import os

CARDS_DIR = os.path.join(os.path.dirname(__file__), "cards")
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
METADATA_FILE = os.path.join(os.path.dirname(__file__), "metadata.json")

# Dominant jersey / national colours per country
COUNTRY_COLOURS = {
    "Argentina": {"bg": "#74ACDF", "accent": "#FFFFFF", "text": "#FFFFFF"},
    "Portugal":  {"bg": "#006600", "accent": "#FF0000", "text": "#FFFFFF"},
    "France":    {"bg": "#002395", "accent": "#ED2939", "text": "#FFFFFF"},
    "Brazil":    {"bg": "#009C3B", "accent": "#FFDF00", "text": "#FFFFFF"},
    "Norway":    {"bg": "#EF2B2D", "accent": "#FFFFFF", "text": "#FFFFFF"},
    "England":   {"bg": "#FFFFFF", "accent": "#CF081F", "text": "#1A1A1A"},
    "Spain":     {"bg": "#AA151B", "accent": "#F1BF00", "text": "#FFFFFF"},
    "Germany":   {"bg": "#000000", "accent": "#DD0000", "text": "#FFFFFF"},
}

# 1080×1920 (9:16 portrait for Shorts), but we output 1080×1920 viewBox
W, H = 1080, 1920


def svg_card(player: dict) -> str:
    country = player["country"]
    colours = COUNTRY_COLOURS.get(country, {"bg": "#222", "accent": "#fff", "text": "#fff"})
    bg      = colours["bg"]
    accent  = colours["accent"]
    text_c  = colours["text"]
    flag    = player["flag"]
    name    = player["name"]
    img_path = os.path.join(IMAGES_DIR, player["image_file"])
    has_img  = os.path.exists(img_path)

    # Image element or placeholder
    if has_img:
        import base64
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = player["image_file"].rsplit(".", 1)[-1].lower()
        mime = "image/png" if ext == "png" else "image/jpeg"
        img_elem = (
            f'<image href="data:{mime};base64,{b64}" '
            f'x="0" y="200" width="{W}" height="1200" '
            f'preserveAspectRatio="xMidYMid slice"/>'
        )
        # Gradient overlay so text is always readable
        overlay = (
            f'<defs>'
            f'<linearGradient id="ov" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{bg}" stop-opacity="0.6"/>'
            f'<stop offset="60%" stop-color="{bg}" stop-opacity="0.0"/>'
            f'<stop offset="100%" stop-color="{bg}" stop-opacity="0.95"/>'
            f'</linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#ov)"/>'
        )
    else:
        img_elem = (
            f'<rect x="0" y="200" width="{W}" height="1200" fill="{bg}" opacity="0.25"/>'
            f'<text x="{W//2}" y="800" font-size="320" text-anchor="middle" '
            f'dominant-baseline="middle">{flag}</text>'
        )
        overlay = ""

    note_line = ""
    if player.get("note"):
        note_line = (
            f'<text x="{W//2}" y="1650" font-family="Arial,sans-serif" '
            f'font-size="46" fill="{accent}" text-anchor="middle" '
            f'font-style="italic">{player["note"]}</text>'
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {W} {H}" width="{W}" height="{H}">

  <!-- Background -->
  <rect width="{W}" height="{H}" fill="{bg}"/>

  <!-- Player image / placeholder -->
  {img_elem}
  {overlay}

  <!-- Top bar -->
  <rect x="0" y="0" width="{W}" height="180" fill="{bg}"/>
  <rect x="0" y="170" width="{W}" height="8" fill="{accent}"/>

  <!-- Flag emoji top-left -->
  <text x="60" y="135" font-size="110" dominant-baseline="middle">{flag}</text>

  <!-- Country name top-right -->
  <text x="{W-60}" y="90" font-family="Arial Black,sans-serif" font-size="72"
        fill="{text_c}" text-anchor="end" font-weight="900">{country}</text>

  <!-- Bottom name plate -->
  <rect x="0" y="1680" width="{W}" height="240" fill="{bg}" opacity="0.92"/>
  <rect x="0" y="1680" width="{W}" height="6" fill="{accent}"/>

  <text x="{W//2}" y="1780" font-family="Arial Black,sans-serif" font-size="96"
        fill="{text_c}" text-anchor="middle" font-weight="900"
        letter-spacing="2">{name.upper()}</text>

  {note_line}
</svg>
"""


def main():
    os.makedirs(CARDS_DIR, exist_ok=True)
    with open(METADATA_FILE) as f:
        players = json.load(f)

    for player in players:
        slug = player["image_file"].replace(".jpg", "").replace(".png", "")
        out_path = os.path.join(CARDS_DIR, f"{slug}.svg")
        svg = svg_card(player)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  [ok] {player['name']} → cards/{slug}.svg")

    print(f"\n{len(players)} cards written to players/cards/")


if __name__ == "__main__":
    main()
