"""
Generates a storyboard sheet for the YouTube Short.
Each panel = one scene, with timestamp, thumbnail, and script line.
Output: players/storyboard.png
"""

import json, math, os, textwrap
from PIL import Image, ImageDraw, ImageFont

CARDS_DIR  = os.path.join(os.path.dirname(__file__), "cards")
OUT_FILE   = os.path.join(os.path.dirname(__file__), "storyboard.png")

# Full scene list keyed to the script
SCENES = [
    dict(ts="0–3s",  label="HOOK",
         line="Do you know which country these legends\nare playing for at World Cup 2026?\nLet's go! 🔥",
         card=None, bg=(20, 20, 20)),

    dict(ts="4–6s",  label="REVEAL #1", line="Messi — Argentina 🇦🇷",    card="messi.png",      bg=(116,172,223)),
    dict(ts="6–8s",  label="REVEAL #2", line="Ronaldo — Portugal 🇵🇹",    card="ronaldo.png",    bg=(0,100,0)),
    dict(ts="8–10s", label="REVEAL #3", line="Mbappé — France 🇫🇷",       card="mbappe.png",     bg=(0,35,149)),
    dict(ts="10–12s",label="REVEAL #4", line="Neymar — Brazil 🇧🇷\n(back after 2 years out!)", card="neymar.png", bg=(0,156,59)),
    dict(ts="12–14s",label="REVEAL #5", line="Haaland — Norway 🇳🇴",      card="haaland.png",    bg=(239,43,45)),
    dict(ts="14–16s",label="REVEAL #6", line="Bellingham — England 🏴󠁧󠁢󠁥󠁮󠁧󠁿", card="bellingham.png", bg=(200,200,220)),
    dict(ts="16–18s",label="REVEAL #7", line="Vinicius Jr — Brazil 🇧🇷",  card="vinicius.png",   bg=(0,156,59)),
    dict(ts="18–19s",label="REVEAL #8", line="Lamine Yamal — Spain 🇪🇸",  card="yamal.png",      bg=(170,21,27)),
    dict(ts="19–20s",label="REVEAL #9", line="Musiala — Germany 🇩🇪",     card="musiala.png",    bg=(20,20,20)),

    dict(ts="21–45s", label="TWIST",
         line="Neymar plays for Al-Hilal…\nbut his COUNTRY? Always Brazil! 🇧🇷\nCould be the LAST WC for Messi & Ronaldo.",
         card=None, bg=(60,10,10)),

    dict(ts="46–60s", label="CTA",
         line="Which player are YOU most excited\nto watch? Comment below! 👇\nLike & subscribe! ⚽🔥",
         card=None, bg=(10,40,10)),
]

# Panel dimensions
PW, PH   = 360, 640      # portrait panel (9:16 mini)
COLS     = 4
PAD      = 24
LABEL_H  = 44
TEXT_H   = 140
INNER_H  = PH - LABEL_H - TEXT_H - PAD * 3

ROWS = math.ceil(len(SCENES) / COLS)
SHEET_W  = COLS * PW + (COLS + 1) * PAD
SHEET_H  = ROWS * PH + (ROWS + 1) * PAD + 60   # +60 for title


def get_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_panel(scene, idx):
    panel = Image.new("RGB", (PW, PH), (15, 15, 15))
    draw  = ImageDraw.Draw(panel)

    # ── label bar ───────────────────────────────────────
    accent = (255, 200, 0)
    draw.rectangle([0, 0, PW, LABEL_H], fill=(30, 30, 30))
    draw.rectangle([0, LABEL_H - 3, PW, LABEL_H], fill=accent)

    fn_label = get_font(16, bold=True)
    draw.text((8, LABEL_H // 2), f"#{idx+1}  {scene['ts']}", font=fn_label,
              fill=(200, 200, 200), anchor="lm")
    draw.text((PW - 8, LABEL_H // 2), scene["label"], font=fn_label,
              fill=accent, anchor="rm")

    # ── image area ──────────────────────────────────────
    img_top  = LABEL_H + PAD
    img_h    = INNER_H
    img_rect = [PAD, img_top, PW - PAD, img_top + img_h]

    # background colour fill
    draw.rectangle(img_rect, fill=scene["bg"])

    if scene["card"]:
        card_path = os.path.join(CARDS_DIR, scene["card"])
        if os.path.exists(card_path):
            card = Image.open(card_path).convert("RGB")
            iw = img_rect[2] - img_rect[0]
            ih = img_rect[3] - img_rect[1]
            card = card.resize((iw, ih), Image.LANCZOS)
            panel.paste(card, (img_rect[0], img_rect[1]))
        else:
            fn_q = get_font(64)
            draw.text(((img_rect[0]+img_rect[2])//2, (img_rect[1]+img_rect[3])//2),
                      "?", font=fn_q, fill=(200,200,200), anchor="mm")
    else:
        # scene number placeholder
        fn_num = get_font(72)
        draw.text(((img_rect[0]+img_rect[2])//2, (img_rect[1]+img_rect[3])//2),
                  scene["label"], font=get_font(22), fill=(180,180,180), anchor="mm")

    # border
    draw.rectangle(img_rect, outline=accent, width=2)

    # ── script text ─────────────────────────────────────
    text_top = img_top + img_h + PAD
    draw.rectangle([0, text_top - 4, PW, PH], fill=(20, 20, 20))
    fn_text = get_font(17)
    y = text_top + 4
    for line in scene["line"].split("\n"):
        draw.text((PW // 2, y), line, font=fn_text, fill=(230, 230, 230), anchor="mt")
        y += 26

    return panel


def main():
    sheet = Image.new("RGB", (SHEET_W, SHEET_H), (8, 8, 8))
    draw  = ImageDraw.Draw(sheet)

    # Title
    fn_title = get_font(28, bold=True)
    draw.text((SHEET_W // 2, 34),
              "STORYBOARD — World Cup 2026 YouTube Short (0–60s)",
              font=fn_title, fill=(255, 200, 0), anchor="mm")

    for i, scene in enumerate(SCENES):
        row = i // COLS
        col = i %  COLS
        x   = PAD + col * (PW + PAD)
        y   = 60 + PAD + row * (PH + PAD)
        panel = draw_panel(scene, i)
        sheet.paste(panel, (x, y))

    sheet.save(OUT_FILE, "PNG", optimize=True)
    kb = os.path.getsize(OUT_FILE) // 1024
    print(f"Storyboard saved → players/storyboard.png  ({kb} KB)")


if __name__ == "__main__":
    main()
