"""Rebuilds the site's images from the game's own art and screenshots.

    python tools/build_assets.py

GAME  : the Godot project (sprite sheets in assets/sprites)
RAW   : dice / pawns / tables exported from the game (see the game repo's notes)
SHOTS : 1920x1080 screenshots of the game
"""
import json
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
GAME = os.environ.get("PIXOPOLY_GAME", "F:/Untitled Game/untitled-card-game")
RAW = os.environ.get("PIXOPOLY_RAW", "F:/Untitled Game/webraw")
SHOTS = os.environ.get("PIXOPOLY_SHOTS", "")
IMG = os.path.join(SITE, "assets", "img")
OUT_SHOTS = os.path.join(SITE, "assets", "shots")


def sheet(name):
    img = Image.open(f"{GAME}/assets/sprites/{name}.png").convert("RGBA")
    atlas = json.load(open(f"{GAME}/assets/sprites/{name}.json"))
    return img, atlas


def cut(sh, key):
    img, atlas = sh
    x, y, w, h = atlas[key]
    return img.crop((x, y, x + w, y + h))


def up(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def strip(images, gap=0):
    w = max(i.width for i in images)
    h = max(i.height for i in images)
    out = Image.new("RGBA", ((w + gap) * len(images), h), (0, 0, 0, 0))
    for n, i in enumerate(images):
        out.alpha_composite(i, (n * (w + gap) + (w - i.width) // 2, h - i.height))
    return out, w, h


def main():
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(OUT_SHOTS, exist_ok=True)
    meta = {}

    # Logo letters (the die goes where the first O would be).
    logo = sheet("logo")
    for ch in "PIXOLY":
        up(cut(logo, ch), 2).save(f"{IMG}/logo_{ch}.png")
    for n in range(1, 7):
        Image.open(f"{RAW}/die_{n}.png").save(f"{IMG}/die_{n}.png")

    # Pawns: 25 columns, 4 rows (idle, breathe, crouch, stretch).
    rows = []
    for fr in (0, 1, 4, 5):
        rows.append([Image.open(f"{RAW}/pawn_{i:02d}_{fr}.png").convert("RGBA") for i in range(25)])
    cw = max(i.width for r in rows for i in r)
    chh = max(i.height for r in rows for i in r)
    pawns = Image.new("RGBA", (cw * 25, chh * 4), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, i in enumerate(r):
            pawns.alpha_composite(i, (x * cw + (cw - i.width) // 2, y * chh + chh - i.height))
    pawns.save(f"{IMG}/pawns.png")
    meta["pawn"] = [cw, chh]

    skins, sw, sh_ = strip([Image.open(f"{RAW}/skin_{i:02d}.png").convert("RGBA") for i in range(27)])
    skins.save(f"{IMG}/skins.png")
    meta["skin"] = [sw, sh_]

    ui = sheet("ui")
    emotes, ew, eh = strip([cut(ui, "emote_" + k) for k in ("laugh", "angry", "wow", "money", "fire", "salt")])
    emotes.save(f"{IMG}/emotes.png")
    meta["emote"] = [ew, eh]
    cards = sheet("cards")
    ab, aw, ah = strip([cut(cards, "ability_" + k) for k in ("extra_roll", "swap", "shield", "sabotage", "steal_house")])
    ab.save(f"{IMG}/abilities.png")
    meta["ability"] = [aw, ah]
    up(cut(cards, "deck_wild"), 2).save(f"{IMG}/deck_wild.png")
    up(cut(cards, "deck_mail"), 2).save(f"{IMG}/deck_mail.png")
    tiles = sheet("tiles")
    for key in ("house", "hotel", "landmark"):
        up(cut(tiles, key), 4).save(f"{IMG}/{key}.png")
    hand = sheet("hand")
    up(cut(hand, "open"), 2).save(f"{IMG}/hand_open.png")

    # The hero's backdrop: the Night City table by itself (no board on it).
    Image.open(f"{RAW}/wide_city.png").convert("RGB").save(f"{IMG}/bg_city.png")

    # Icons from the logo die.
    die = Image.open(f"{RAW}/die_5.png").convert("RGBA")
    for size in (32, 180, 192, 512):
        canvas = Image.new("RGBA", (size, size), (33, 24, 20, 255))
        k = max(1, (size * 3 // 4) // die.width) if size >= 180 else 1
        d = up(die, k) if size >= 180 else die.resize((size - 4, size - 4), Image.NEAREST)
        canvas.alpha_composite(d, ((size - d.width) // 2, (size - d.height) // 2))
        canvas.save(f"{IMG}/icon-{size}.png")
    Image.open(f"{IMG}/icon-32.png").save(os.path.join(SITE, "favicon.ico"), sizes=[(32, 32)])

    # Screenshots: full size (lossless WebP) and a small one for the page.
    if SHOTS and os.path.isdir(SHOTS):
        for f in sorted(os.listdir(SHOTS)):
            if not f.endswith(".png") or f.startswith("sheet"):
                continue
            im = Image.open(os.path.join(SHOTS, f)).convert("RGB")
            name = f[:-4]
            im.save(f"{OUT_SHOTS}/{name}.webp", lossless=True, method=6)
            # Half size, nearest: the art's pixels are 2 px, so this stays crisp
            # (and lossless pixel art is smaller than a lossy copy).
            im.resize((960, 540), Image.NEAREST).save(f"{OUT_SHOTS}/{name}_s.webp", lossless=True, method=6)
        # The share picture: the board with the logo over it.
        board = Image.open(os.path.join(SHOTS, "board_city.png")).convert("RGBA")
        og = board.resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652))
        shade = Image.new("RGBA", og.size, (16, 12, 24, 150))
        og = Image.alpha_composite(og, shade)
        letters = [up(cut(logo, c), 2) if c != "*" else Image.open(f"{RAW}/die_5.png").convert("RGBA") for c in "PIX*POLY"]
        total = sum(i.width for i in letters) + 6 * 7
        x = (1200 - total) // 2
        for i in letters:
            og.alpha_composite(i, (x, 240 + (146 - i.height)))
            x += i.width + 6
        og.convert("RGB").save(f"{IMG}/og.png")

    json.dump(meta, open(os.path.join(SITE, "assets", "sprites.json"), "w"))
    print("assets built", meta)


if __name__ == "__main__":
    sys.exit(main())
