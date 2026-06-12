"""
Generates a YouTube Shorts MP4 (1080x1920, 30fps, ~35s).

Run from the repo root:
    python3 players/make_video.py

Output: players/world_cup_short.mp4

Requires:  pip install moviepy pillow
Real photos improve quality but placeholders work too —
just run `python3 players/download.py` first.
"""

import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import VideoClip, concatenate_videoclips

W, H  = 1080, 1920
FPS   = 30
DIR   = os.path.dirname(os.path.abspath(__file__))
CARDS  = os.path.join(DIR, "cards")
IMAGES = os.path.join(DIR, "images")
OUT    = os.path.join(DIR, "world_cup_short.mp4")

THEMES = {
    "Argentina": dict(c1=(116,172,223), c2=(255,255,255), accent=(255,255,255)),
    "Portugal":  dict(c1=(0,100,0),     c2=(196,0,0),     accent=(255,215,0)),
    "France":    dict(c1=(0,35,149),    c2=(237,41,57),   accent=(255,255,255)),
    "Brazil":    dict(c1=(0,156,59),    c2=(255,223,0),   accent=(255,223,0)),
    "Norway":    dict(c1=(239,43,45),   c2=(255,255,255), accent=(0,50,160)),
    "England":   dict(c1=(200,200,220), c2=(207,8,31),    accent=(207,8,31)),
    "Spain":     dict(c1=(170,21,27),   c2=(241,191,0),   accent=(241,191,0)),
    "Germany":   dict(c1=(20,20,20),    c2=(221,0,0),     accent=(255,206,0)),
}

PLAYERS = [
    dict(name="Lionel Messi",      country="Argentina", flag="🇦🇷", slug="messi",       dur=2.0),
    dict(name="Cristiano Ronaldo", country="Portugal",  flag="🇵🇹", slug="ronaldo",     dur=2.0),
    dict(name="Kylian Mbappé",     country="France",    flag="🇫🇷", slug="mbappe",      dur=2.0),
    dict(name="Neymar Jr",         country="Brazil",    flag="🇧🇷", slug="neymar",      dur=2.0, note="back after 2 years!"),
    dict(name="Erling Haaland",    country="Norway",    flag="🇳🇴", slug="haaland",     dur=2.0),
    dict(name="Jude Bellingham",   country="England",   flag="🏴󠁧󠁢󠁥󠁮󠁧󠁿", slug="bellingham",  dur=2.0),
    dict(name="Vinicius Jr",       country="Brazil",    flag="🇧🇷", slug="vinicius",    dur=2.0),
    dict(name="Lamine Yamal",      country="Spain",     flag="🇪🇸", slug="yamal",       dur=1.5),
    dict(name="Jamal Musiala",     country="Germany",   flag="🇩🇪", slug="musiala",     dur=1.5),
]


# ── helpers ──────────────────────────────────────────────────────────────────

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

def lerp(a, b, t):
    return a + (b - a) * t

def ease_out(t):
    return 1 - (1 - t) ** 3

def ease_in_out(t):
    return t * t * (3 - 2 * t)

def pil_to_np(img):
    return np.array(img.convert("RGB"))

def load_photo(slug, theme):
    """
    Load the real player photo and cover-crop to 1080x1920.
    Falls back to a country-coloured placeholder if missing.
    """
    for ext in ("jpg", "jpeg", "png"):
        path = os.path.join(IMAGES, f"{slug}.{ext}")
        if os.path.exists(path):
            photo = Image.open(path).convert("RGB")
            pw, ph = photo.size
            scale  = max(W / pw, H / ph)
            nw, nh = int(pw * scale), int(ph * scale)
            photo  = photo.resize((nw, nh), Image.LANCZOS)
            x0 = (nw - W) // 2
            y0 = max(0, min((nh - H) // 4, nh - H))
            print(f"    ✓ photo loaded: {path}  ({pw}x{ph} → cropped to {W}x{H})")
            return photo.crop((x0, y0, x0 + W, y0 + H))

    print(f"    ✗ NO photo for '{slug}' — using placeholder  (expected: {IMAGES}/{slug}.jpg)")
    c1 = theme["c1"]
    img = Image.new("RGB", (W, H), c1)
    d   = ImageDraw.Draw(img)
    d.text((W//2, H//2), slug.upper(), font=get_font(120), fill=(255,255,255), anchor="mm")
    return img


# ── scene builders ───────────────────────────────────────────────────────────

def zoom_frame(base_img, t, dur, zoom_start=1.18, zoom_end=1.0):
    """Ken Burns zoom-in effect."""
    progress = ease_out(min(t / max(dur * 0.6, 0.01), 1.0))
    scale = lerp(zoom_start, zoom_end, progress)
    nw = int(W * scale)
    nh = int(H * scale)
    resized = base_img.resize((nw, nh), Image.BILINEAR)
    x0 = (nw - W) // 2
    y0 = (nh - H) // 2
    return resized.crop((x0, y0, x0 + W, y0 + H))


def add_caption(img, player, t, dur, theme):
    """Big slide-up name + country plate — fills bottom third of screen."""
    accent = theme["accent"]
    c1     = theme["c1"]

    slide_progress = ease_out(min(t / 0.4, 1.0))
    fade           = min(t / 0.25, 1.0)

    plate_h      = 420                          # tall plate — bottom third
    plate_y      = H - plate_h
    slide_offset = int((1 - slide_progress) * 200)

    # dark plate
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([0, plate_y + slide_offset, W, H + 10],
                 fill=(*[max(0, v - 10) for v in c1], int(245 * fade)))
    # thick accent bar on top edge
    od.rectangle([0, plate_y + slide_offset, W, plate_y + slide_offset + 12],
                 fill=(*accent, int(255 * fade)))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    y_base = plate_y + slide_offset

    # ── PLAYER NAME — very large ──────────────────────────────────────────
    fn_name = get_font(148)
    name    = player["name"].upper()
    # auto-shrink if name is long
    while True:
        bb = draw.textbbox((0, 0), name, font=fn_name)
        if bb[2] - bb[0] <= W - 60 or fn_name.size <= 80:
            break
        fn_name = get_font(fn_name.size - 10)

    # drop shadow
    draw.text((W // 2 + 4, y_base + 120 + 4), name,
              font=fn_name, fill=(0, 0, 0), anchor="mm")
    draw.text((W // 2,     y_base + 120),     name,
              font=fn_name, fill=(255, 255, 255), anchor="mm")

    # ── COUNTRY — large accent colour ─────────────────────────────────────
    fn_country  = get_font(96)
    country_str = player["country"].upper()
    draw.text((W // 2 + 3, y_base + 260 + 3), country_str,
              font=fn_country, fill=(0, 0, 0), anchor="mm")
    draw.text((W // 2,     y_base + 260),     country_str,
              font=fn_country, fill=accent, anchor="mm")

    # optional note (smaller, below country)
    if player.get("note"):
        fn_note = get_font(58)
        draw.text((W // 2, y_base + 360), player["note"].upper(),
                  font=fn_note, fill=(220, 220, 220), anchor="mm")

    return img


def add_top_bar(img, ts_text, country, theme):
    c1     = theme["c1"]
    accent = theme["accent"]
    bar    = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd     = ImageDraw.Draw(bar)
    bd.rectangle([0, 0, W, 160], fill=(*[max(0, v - 15) for v in c1], 220))
    bd.rectangle([0, 154, W, 162], fill=(*accent, 255))
    img  = Image.alpha_composite(img.convert("RGBA"), bar).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.text((W - 50, 80), country.upper(), font=get_font(68), fill=(255, 255, 255), anchor="rm")
    draw.text((50,     80), ts_text,         font=get_font(52), fill=accent,           anchor="lm")
    return img


def player_clip(player, theme, ts_label):
    card = load_photo(player["slug"], theme)
    dur  = player["dur"]

    def make_frame(t):
        frame = zoom_frame(card, t, dur)
        # Light gradient: only darken the top bar area and bottom caption area.
        # The middle (player's face/body) stays fully visible.
        grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd   = ImageDraw.Draw(grad)
        for y in range(H):
            # top 180px: fade from 160 alpha → 0
            t_top    = max(0.0, 1.0 - y / 180)
            # bottom 500px: fade from 0 → 200 alpha
            t_bottom = max(0.0, (y - (H - 500)) / 500)
            alpha    = int(160 * t_top + 200 * t_bottom ** 1.5)
            if alpha > 0:
                gd.line([(0, y), (W, y)], fill=(0, 0, 0, min(alpha, 210)))
        frame = Image.alpha_composite(frame.convert("RGBA"), grad).convert("RGB")
        frame = add_top_bar(frame, ts_label, player["country"], theme)
        frame = add_caption(frame, player, t, dur, theme)
        return pil_to_np(frame)

    return VideoClip(make_frame, duration=dur)


def text_scene(lines, bg_color, dur, accent=(255,200,0), line_dur=0.55):
    """Animated text reveal, one line at a time."""
    fn_big  = get_font(96)
    fn_small= get_font(68)
    base_bg = Image.new("RGB", (W, H), bg_color)

    # subtle gradient
    gd = ImageDraw.Draw(base_bg)
    darker = tuple(max(0, v - 40) for v in bg_color)
    for y in range(H):
        t_g = y / H
        col = tuple(int(bg_color[i] + (darker[i] - bg_color[i]) * t_g) for i in range(3))
        gd.line([(0,y),(W,y)], fill=col)

    def make_frame(t):
        img  = base_bg.copy()
        draw = ImageDraw.Draw(img)

        total_h = len(lines) * 100
        start_y = H // 2 - total_h // 2

        for i, (line, big) in enumerate(lines):
            appear_t = i * line_dur
            if t < appear_t:
                continue
            alpha_t = min((t - appear_t) / 0.3, 1.0)
            slide_t = ease_out(min((t - appear_t) / 0.35, 1.0))
            slide_y = int((1 - slide_t) * 40)

            fn = fn_big if big else fn_small
            col = accent if big else (230, 230, 230)
            # shadow
            draw.text((W//2 + 3, start_y + i*100 + slide_y + 3),
                      line, font=fn, fill=(0,0,0), anchor="mm")
            draw.text((W//2, start_y + i*100 + slide_y),
                      line, font=fn, fill=col, anchor="mm")

        # accent bar
        draw.rectangle([W//2 - 80, H - 90, W//2 + 80, H - 84], fill=accent)
        return pil_to_np(img)

    return VideoClip(make_frame, duration=dur)


def flash_transition(dur=0.12):
    """Quick white flash between scenes."""
    def make_frame(t):
        alpha = int(255 * (1 - t / dur) ** 2)
        arr = np.full((H, W, 3), alpha, dtype=np.uint8)
        return arr
    return VideoClip(make_frame, duration=dur)


# ── assemble ──────────────────────────────────────────────────────────────────

def build():
    clips = []
    flash = flash_transition(0.10)

    # 1. HOOK
    print("  Building HOOK …")
    hook_lines = [
        ("WORLD CUP 2026 ⚽", True),
        ("Do you know which country", False),
        ("these legends play for?", False),
        ("", False),
        ("LET'S GO! 🔥", True),
    ]
    clips.append(text_scene(hook_lines, (10,10,30), dur=3.0,
                             accent=(255,200,0), line_dur=0.45))
    clips.append(flash_transition(0.10))

    # 2. Player reveals
    for i, player in enumerate(PLAYERS):
        country = player["country"]
        theme   = THEMES.get(country, dict(c1=(30,30,30), c2=(80,80,80), accent=(255,200,0)))
        ts      = f"#{i+1}/9"
        print(f"  Building {player['name']} …")
        clips.append(player_clip(player, theme, ts))
        clips.append(flash_transition(0.08))

    # 3. TWIST
    print("  Building TWIST …")
    twist_lines = [
        ("THE ONE EVERYONE", True),
        ("GETS WRONG... 🤔", True),
        ("", False),
        ("Neymar plays for Al-Hilal…", False),
        ("but his COUNTRY?", False),
        ("ALWAYS BRAZIL! 🇧🇷", True),
        ("", False),
        ("Could be the LAST WC", False),
        ("for Messi & Ronaldo.", False),
    ]
    clips.append(text_scene(twist_lines, (50,5,5), dur=5.5,
                             accent=(255,80,80), line_dur=0.48))
    clips.append(flash_transition(0.10))

    # 4. CTA
    print("  Building CTA …")
    cta_lines = [
        ("COMMENT BELOW! 👇", True),
        ("Which player are YOU", False),
        ("most excited to watch?", False),
        ("", False),
        ("LIKE & SUBSCRIBE ⚽🔥", True),
    ]
    clips.append(text_scene(cta_lines, (5,40,5), dur=4.0,
                             accent=(80,255,120), line_dur=0.5))

    print("  Concatenating clips …")
    final = concatenate_videoclips(clips)

    print(f"  Writing {OUT} …")
    final.write_videofile(
        OUT,
        fps=FPS,
        codec="libx264",
        audio=False,
        preset="fast",
        ffmpeg_params=["-crf", "23", "-pix_fmt", "yuv420p"],
        logger="bar",
    )
    mb = os.path.getsize(OUT) / 1024 / 1024
    print(f"\nDone!  {OUT}  ({mb:.1f} MB)")
    print("Upload directly to YouTube Shorts (vertical 1080×1920).")


if __name__ == "__main__":
    build()
