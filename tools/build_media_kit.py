"""Builds the social media kit: pictures for Instagram and X, in the game's
own art, plus a zip of the lot.

    python tools/build_media_kit.py

Everything is drawn from the site's assets (assets/img, assets/shots) and the
raw table art, with the game's font at whole multiples of its size, so the
pictures are as crisp as the game.
"""
import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
IMG = os.path.join(SITE, "assets", "img")
SHOTS = os.path.join(SITE, "assets", "shots")
RAW = os.environ.get("PIXOPOLY_RAW", "F:/Untitled Game/webraw")
OUT = os.path.join(SITE, "media-kit")
FONT = os.path.join(SITE, "assets", "fonts", "PixelOperator-Bold.ttf")

INK = (18, 19, 31)
NIGHT = (23, 26, 46)
WALNUT = (38, 43, 71)        # (slate now: the game's panels)
RIM = (52, 59, 98)
COPPER = (232, 117, 42)      # (the game's orange)
GOLD = (255, 216, 102)
PARCH = (246, 237, 216)
WHITE = (255, 248, 224)
PINK = (232, 106, 166)
GREEN = (52, 163, 90)
TEAL = (31, 163, 155)
RED = (220, 74, 68)

PAWNS = ["Pawn", "Top Hat", "Car", "Cat", "Boat", "Castle", "Crown", "Rocket", "Duck", "Dog", "Robot", "Ghost", "Dino",
         "Penguin", "Frog", "Teapot", "Skateboard", "UFO", "Boot", "Cactus", "Mushroom", "Alien", "Crab", "Pumpkin", "Slime"]


def font(size):
    return ImageFont.truetype(FONT, size)


def up(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def load(name):
    return Image.open(os.path.join(IMG, name)).convert("RGBA")


def pawn(n, k=8, frame=0):
    sheet = load("pawns.png")
    return up(sheet.crop((n * 20, frame * 24, n * 20 + 20, frame * 24 + 24)), k)


def skin(n, k=2):
    sheet = load("skins.png")
    return up(sheet.crop((n * 60, 0, n * 60 + 60, 60)), k)


def backdrop(size, theme="city", dim=0.0):
    """A table's art filling the picture (whole-number scale, cropped to fit)."""
    src = Image.open(f"{RAW}/wide_{theme}.png").convert("RGB")
    k = max(1, -(-size[0] // src.width), -(-size[1] // src.height))
    big = src.resize((src.width * k, src.height * k), Image.NEAREST)
    x = (big.width - size[0]) // 2
    y = big.height - size[1] if theme == "city" else (big.height - size[1]) // 2
    out = big.crop((x, y, x + size[0], y + size[1])).convert("RGBA")
    if dim > 0:
        out = Image.alpha_composite(out, Image.new("RGBA", size, NIGHT + (int(255 * dim),)))
    return out


def text(d, xy, s, size, fill=WHITE, shadow=INK, anchor="la", depth=None):
    """Hard-edged pixel text with a solid drop shadow."""
    d.fontmode = "1"
    f = font(size)
    depth = depth if depth is not None else max(2, size // 16 * 2)
    if shadow:
        d.text((xy[0] + depth, xy[1] + depth), s, font=f, fill=shadow, anchor=anchor)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def wrap(s, size, width):
    f = font(size)
    lines, line = [], ""
    for word in s.split():
        trial = (line + " " + word).strip()
        if f.getlength(trial) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def block(d, xy, s, size, width, fill=WHITE, shadow=INK, center=False, gap=1.2):
    """Wrapped text; returns the y below it."""
    x, y = xy
    for line in wrap(s, size, width):
        if center:
            text(d, (x + width // 2, y), line, size, fill, shadow, anchor="ma")
        else:
            text(d, (x, y), line, size, fill, shadow)
        y += int(size * gap)
    return y


def panel(img, box, fill=WALNUT, rim=RIM, u=8):
    """The game's frame: ink, one thick flat rim, then the fill, with a hard shadow."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    d.rectangle((x0 + u * 2, y0 + u * 3, x1 + u * 2, y1 + u * 3), fill=(0, 0, 0, 110))
    d.rectangle((x0 - u * 3, y0 - u * 3, x1 + u * 3, y1 + u * 3), fill=INK)
    d.rectangle((x0 - u * 2, y0 - u * 2, x1 + u * 2, y1 + u * 2), fill=rim)   # one thick flat slab
    d.rectangle(box, fill=fill)


def tag(img, xy, s, size=32, fill=COPPER, ink=INK, center=False):
    """A flat label, like the site's kickers."""
    d = ImageDraw.Draw(img)
    w = int(font(size).getlength(s))
    x, y = xy
    if center:
        x -= (w + size) // 2
    d.rectangle((x - 6, y - 6, x + w + size + 6, y + size + 14), fill=INK)
    d.rectangle((x, y, x + w + size, y + size + 8), fill=fill)
    d.fontmode = "1"
    d.text((x + size // 2, y + 2), s, font=font(size), fill=ink)
    return w + size


def logo(img, cx, y, k=1, die=5):
    """PIX(die)POLY centred on cx. k scales the letters (they're 116x146 at 1)."""
    parts = []
    for ch in "PIX*POLY":
        p = Image.open(f"{RAW}/die_{die}.png").convert("RGBA") if ch == "*" else load(f"logo_{ch}.png")
        parts.append(up(p, k) if k > 1 else p)
    gap = 4 * k
    total = sum(p.width for p in parts) + gap * (len(parts) - 1)
    x = cx - total // 2
    h = max(p.height for p in parts)
    for p in parts:
        shadow = Image.new("RGBA", p.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 90), mask=p.split()[3])
        img.alpha_composite(shadow, (x + 8 * k, y + h - p.height + 10 * k))
        img.alpha_composite(p, (x, y + h - p.height))
        x += p.width + gap
    return total, h


def paste_center(img, sprite, cx, cy):
    img.alpha_composite(sprite, (cx - sprite.width // 2, cy - sprite.height // 2))


def shot(name):
    return Image.open(os.path.join(SHOTS, name + ".webp")).convert("RGBA")


def framed(img, picture, box):
    panel(img, box, fill=INK)
    fit = picture.resize((box[2] - box[0], box[3] - box[1]), Image.NEAREST)
    img.alpha_composite(fit, (box[0], box[1]))


def footer(img, soon="COMING SOON TO STEAM"):
    d = ImageDraw.Draw(img)
    w, h = img.size
    d.rectangle((0, h - 92, w, h), fill=WALNUT)
    d.rectangle((0, h - 100, w, h - 92), fill=RIM)
    d.rectangle((0, h - 108, w, h - 100), fill=INK)
    text(d, (40, h - 74), "PIXOPOLY", 48, GOLD)
    text(d, (w - 40, h - 66), soon, 32, PARCH, anchor="ra")


# ─── The pictures ─────────────────────────────────────────────────────────────

def announce(size, name, k=1):
    img = backdrop(size, "city", 0.15)
    d = ImageDraw.Draw(img)
    w, h = size
    _, lh = logo(img, w // 2, int(h * 0.26), k)
    y = int(h * 0.26) + lh + 40
    y = block(d, (60, y), "Buy the world. Bankrupt your friends.", 64 if w >= 1080 else 48, w - 120, center=True)
    tag(img, (w // 2, y + 30), "COMING SOON TO STEAM", 32, GOLD, center=True)
    # A few pawns standing along the street.
    picks = [14, 0, 15, 10, 3, 16]
    step = w // (len(picks) + 1)
    for i, n in enumerate(picks):
        p = pawn(n, 8)
        img.alpha_composite(p, (step * (i + 1) - p.width // 2, h - p.height - 36))
    img.convert("RGB").save(os.path.join(OUT, name))


def toronto(size, name):
    img = backdrop(size, "table", 0.45)
    d = ImageDraw.Draw(img)
    w, h = size
    wide = w > h
    tag(img, (60, 60), "THE GAME YOU KNOW", 32)
    y = block(d, (60, 150), "Charge your best friend $950 for one night in Toronto.", 96 if not wide else 80, w - 120 if not wide else int(w * 0.55), gap=1.15)
    block(d, (60, y + 26), "They'll forgive you. Eventually.", 48, w - 120, fill=GOLD)
    hotel = up(load("hotel.png"), 3)
    house = up(load("house.png"), 3)
    if wide:
        paste_center(img, hotel, int(w * 0.8), int(h * 0.36))
        for i in range(4):
            paste_center(img, house, int(w * 0.8) - int(1.5 * (house.width + 14)) + i * (house.width + 14), int(h * 0.68))
    else:
        paste_center(img, hotel, w // 2, h - 380)
        for i in range(4):
            paste_center(img, house, w // 2 - int(1.5 * (house.width + 16)) + i * (house.width + 16), h - 210)
    footer(img)
    img.convert("RGB").save(os.path.join(OUT, name))


def pawns_post(size, name):
    img = Image.new("RGBA", size, (42, 143, 138, 255))
    d = ImageDraw.Draw(img)
    w, h = size
    for yy in range(0, h, 56):                 # the felt's polka dots
        for xx in range(0, w, 56):
            d.rectangle((xx + 20, yy + 20, xx + 31, yy + 31), fill=(26, 92, 89))
    wide = w > h
    cols = 9 if wide else 5
    k = 6
    picks = list(range(25))[: cols * (2 if wide else 4)]
    cell = (w - 120) // cols
    top = 250
    for i, n in enumerate(picks):
        p = pawn(n, k)
        cx = 60 + cell // 2 + (i % cols) * cell
        cy = top + (i // cols) * (p.height + 26) + p.height // 2
        d.rectangle((cx - p.width // 2 + 10, cy + p.height // 2 - 6, cx + p.width // 2 - 2, cy + p.height // 2 + 6), fill=(26, 92, 89))
        paste_center(img, p, cx, cy)
    tag(img, (60, 50), "25 PAWNS. 27 DICE. ZERO SHOPS.", 32, GOLD)
    block(d, (60, 130), "Be a frog. Be a teapot. Be a skateboard.", 64 if not wide else 64, w - 120)
    footer(img, "EVERYTHING IS EARNED BY PLAYING")
    img.convert("RGB").save(os.path.join(OUT, name))


def chaos(size, name):
    img = backdrop(size, "space", 0.2)
    d = ImageDraw.Draw(img)
    w, h = size
    tag(img, (w // 2, 70), "CHAOS MODE", 32, PINK, center=True)
    y = block(d, (60, 170), "Round 7.", 96, w - 120, center=True)
    # The stamp, tilted like the one in the game.
    stamp = Image.new("RGBA", (int(font(96).getlength("EARTHQUAKE")) + 120, 190), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle((0, 0, stamp.width - 1, stamp.height - 1), fill=INK)
    sd.rectangle((10, 10, stamp.width - 11, stamp.height - 11), fill=PINK)
    sd.fontmode = "1"
    sd.text((stamp.width // 2 + 6, stamp.height // 2 + 2), "EARTHQUAKE", font=font(96), fill=INK, anchor="mm")
    sd.text((stamp.width // 2, stamp.height // 2 - 4), "EARTHQUAKE", font=font(96), fill=WHITE, anchor="mm")
    stamp = stamp.rotate(6, expand=True, resample=Image.NEAREST)
    if stamp.width > w - 40:
        stamp = stamp.resize((w - 40, int(stamp.height * (w - 40) / stamp.width)), Image.NEAREST)
    paste_center(img, stamp, w // 2, y + 150)
    y2 = y + 320
    y2 = block(d, (60, y2), "Everyone loses a building.", 48, w - 120, center=True)
    block(d, (60, y2 + 10), "Your plans: cancelled.", 48, w - 120, fill=GOLD, center=True)
    em = up(load("emotes.png"), 8)
    for i, n in enumerate([2, 1, 5]):
        face = em.crop((n * 144, 0, n * 144 + 144, 144))
        if w > h:      # landscape: the faces watch from the corners instead
            paste_center(img, face, [170, w - 170, w - 170][i], [250, 250, 560][i])
        else:
            paste_center(img, face, w // 2 + (i - 1) * 200, h - 250)
    footer(img, "ONE WILD EVENT EVERY ROUND")
    img.convert("RGB").save(os.path.join(OUT, name))


def screenshot_post(size, name, which, kicker, line):
    img = backdrop(size, "city", 0.5)
    d = ImageDraw.Draw(img)
    w, h = size
    tag(img, (60, 56), kicker, 32, COPPER)
    y = block(d, (60, 140), line, 64, w - 120, gap=1.15)
    pic = shot(which)
    bw = w - 160
    bh = bw * 9 // 16
    top = max(y + 50, (h - 100 - bh) // 2 + 60)
    framed(img, pic, (80, top, 80 + bw, top + bh))
    footer(img)
    img.convert("RGB").save(os.path.join(OUT, name))


def rules_story(size, name):
    img = backdrop(size, "table", 0.5)
    d = ImageDraw.Draw(img)
    w, h = size
    logo(img, w // 2, 150, 1)
    box = (90, 430, w - 90, 1420)
    panel(img, box, fill=PARCH)
    text(d, (w // 2, 470), "HOUSE RULES", 64, RED, shadow=None, anchor="ma")
    text(d, (w // 2, 540), "OF FRIENDSHIP", 64, RED, shadow=None, anchor="ma")
    rules = ["No mercy on rent.", "A trade is a trade.", "The bank is not your mum.", "Whoever flips the board buys the snacks."]
    y = 680
    for i, r in enumerate(rules):
        text(d, (140, y), f"{i + 1}.", 48, RED, shadow=None)
        y = block(d, (220, y), r, 48, w - 220 - 140, fill=INK, shadow=None, gap=1.15) + 40
    for i, n in enumerate([14, 15, 3, 10]):
        p = pawn(n, 10)
        img.alpha_composite(p, (110 + i * 230, 1500))
    tag(img, (w // 2, 1790), "COMING SOON TO STEAM", 32, GOLD, center=True)
    img.convert("RGB").save(os.path.join(OUT, name))


def story_announce(size, name):
    img = backdrop(size, "city", 0.2)
    d = ImageDraw.Draw(img)
    w, h = size
    logo(img, w // 2, 300, 1)
    y = block(d, (60, 520), "Buy the world.", 96, w - 120, center=True)
    y = block(d, (60, y), "Bankrupt your friends.", 80, w - 120, fill=GOLD, center=True)
    pic = shot("board_city")
    bw = w - 120
    framed(img, pic, (60, y + 80, 60 + bw, y + 80 + bw * 9 // 16))
    y2 = y + 80 + bw * 9 // 16 + 110
    block(d, (60, y2), "2 to 6 players. Online, on your network, or one mouse on the couch.", 48, w - 120, center=True)
    tag(img, (w // 2, h - 200), "COMING SOON TO STEAM", 32, GOLD, center=True)
    img.convert("RGB").save(os.path.join(OUT, name))


def header(size, name):
    img = backdrop(size, "city", 0.1)
    d = ImageDraw.Draw(img)
    w, h = size
    logo(img, w // 2, 70, 1)
    text(d, (w // 2, 250), "Buy the world. Bankrupt your friends.", 48, WHITE, anchor="ma")
    for i, n in enumerate([14, 0, 15, 10, 3, 16, 12, 20, 7, 23, 11, 8]):
        p = pawn(n, 6)
        img.alpha_composite(p, (30 + i * 122, h - p.height - 10))
    img.convert("RGB").save(os.path.join(OUT, name))


def avatar(px, name):
    img = Image.new("RGBA", (px, px), WALNUT + (255,))
    d = ImageDraw.Draw(img)
    u = px // 50
    d.rectangle((0, 0, px - 1, px - 1), fill=INK)
    d.rectangle((u, u, px - 1 - u, px - 1 - u), fill=GOLD)
    d.rectangle((u * 2, u * 2, px - 1 - u * 2, px - 1 - u * 2), fill=INK)
    d.rectangle((u * 3, u * 3, px - 1 - u * 3, px - 1 - u * 3), fill=(42, 143, 138))
    die = Image.open(f"{RAW}/die_5.png").convert("RGBA")
    k = max(1, int(px * 0.62) // die.width)
    paste_center(img, up(die, k), px // 2, px // 2)
    img.convert("RGB").save(os.path.join(OUT, name))



# ─── Logos ────────────────────────────────────────────────────────────────────

GAME = os.environ.get("PIXOPOLY_GAME", "F:/Untitled Game/untitled-card-game")
FELT = (42, 143, 138)


def logo_parts(die=5):
    return [Image.open(f"{RAW}/die_{die}.png").convert("RGBA") if ch == "*" else load(f"logo_{ch}.png") for ch in "PIX*POLY"]


def wordmark(k=1, shadow=True, mono=None, gap=4):
    """The logo on its own, transparent: PIX(die)POLY. mono = one flat colour
    (for stamping over photos or printing)."""
    parts = [up(p, k) if k > 1 else p for p in logo_parts()]
    g = gap * k
    sh = 10 * k if shadow else 0
    w = sum(p.width for p in parts) + g * (len(parts) - 1) + sh
    h = max(p.height for p in parts) + sh
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x = 0
    for p in parts:
        y = h - sh - p.height
        if mono:
            mask = p.split()[3]
            if p.width == p.height:   # the die: its pips and light faces cut out, so it still reads as a die
                px = p.load()
                mask = mask.copy()
                mp = mask.load()
                for yy in range(p.height):
                    for xx in range(p.width):
                        r, g_, b, a = px[xx, yy]
                        if a and (r + g_ + b) / 3 > 150:
                            mp[xx, yy] = 0
            flat = Image.new("RGBA", p.size, mono + (255,))
            img.paste(flat, (x, y), mask=mask)
        else:
            if shadow:
                drop = Image.new("RGBA", p.size, (0, 0, 0, 0))
                drop.paste((0, 0, 0, 110), mask=p.split()[3])
                img.alpha_composite(drop, (x + sh * 8 // 10, y + sh))
            img.alpha_composite(p, (x, y))
        x += p.width + g
    return img


def stacked(k=1, shadow=True):
    """PIX(die) over POLY: for square spaces."""
    parts = [up(p, k) if k > 1 else p for p in logo_parts()]
    top, bottom = parts[:4], parts[4:]
    g = 4 * k
    sh = 10 * k if shadow else 0
    lh = max(p.height for p in parts)
    rows = [top, bottom]
    w = max(sum(p.width for p in r) + g * (len(r) - 1) for r in rows) + sh
    h = lh * 2 + 18 * k + sh
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for ri, r in enumerate(rows):
        rw = sum(p.width for p in r) + g * (len(r) - 1)
        x = (w - sh - rw) // 2
        for p in r:
            y = ri * (lh + 18 * k) + lh - p.height
            if shadow:
                drop = Image.new("RGBA", p.size, (0, 0, 0, 0))
                drop.paste((0, 0, 0, 110), mask=p.split()[3])
                img.alpha_composite(drop, (x + sh * 8 // 10, y + sh))
            img.alpha_composite(p, (x, y))
            x += p.width + g
    return img


def on(bg, art, size, pad_y=0):
    img = Image.new("RGBA", size, bg + (255,))
    paste_center(img, art, size[0] // 2, size[1] // 2 + pad_y)
    return img


def die_icon(px, bg=None, rim=True):
    """The red-and-cream die from the logo, on the felt with a gold rim (or
    transparent). Its content keeps clear of a circle crop."""
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0) if bg is None else bg + (255,))
    d = ImageDraw.Draw(img)
    if bg is not None and rim:
        u = max(1, px // 50)
        d.rectangle((0, 0, px - 1, px - 1), fill=INK)
        d.rectangle((u, u, px - 1 - u, px - 1 - u), fill=GOLD)
        d.rectangle((u * 2, u * 2, px - 1 - u * 2, px - 1 - u * 2), fill=INK)
        d.rectangle((u * 3, u * 3, px - 1 - u * 3, px - 1 - u * 3), fill=bg)
    die = Image.open(f"{RAW}/die_5.png").convert("RGBA")
    k = max(1, int(px * (0.55 if bg is not None else 0.92)) // die.width)
    paste_center(img, up(die, k), px // 2, px // 2)
    return img


def logos():
    out = os.path.join(OUT, "logos")
    os.makedirs(out, exist_ok=True)
    save = lambda im, n: im.save(os.path.join(out, n))
    for k in (1, 2, 4):
        save(wordmark(k), f"wordmark-{k}x.png")
    save(wordmark(2, shadow=False, mono=WHITE), "wordmark-white.png")
    save(wordmark(2, shadow=False, mono=INK), "wordmark-black.png")
    save(wordmark(2, shadow=False, mono=GOLD), "wordmark-gold.png")
    save(on(NIGHT, wordmark(2), (2400, 800)), "wordmark-on-dark.png")
    save(on(PARCH, wordmark(2), (2400, 800)), "wordmark-on-light.png")
    save(on(FELT, wordmark(2), (2400, 800)), "wordmark-on-felt.png")
    save(stacked(2), "stacked-2x.png")
    save(on(NIGHT, stacked(2), (1200, 1200)), "stacked-on-dark.png")
    save(on(PARCH, stacked(2), (1200, 1200)), "stacked-on-light.png")
    for px in (512, 1024):
        save(die_icon(px), f"die-{px}.png")
        save(die_icon(px, FELT), f"app-icon-{px}.png")
    save(die_icon(1024, NIGHT), "app-icon-dark-1024.png")


# ─── Profile pictures and banners for every platform ─────────────────────────

def city_strip(names, k):
    pics = [up(Image.open(f"{GAME}/assets/sprites/cities/card/{c}.png").convert("RGBA"), k) for c in names]
    return pics


def banner(size, name, logo_k=1, safe=None, line=True, pawns=True):
    """The logo over the night city, pawns along the street. `safe` = the box
    every platform keeps visible (content stays inside it)."""
    img = backdrop(size, "city", 0.15)
    d = ImageDraw.Draw(img)
    w, h = size
    sx, sy, sw, shh = safe or (0, 0, w, h)
    mark = wordmark(logo_k)
    if mark.width > sw * 0.8:
        mark = wordmark(1)
    cy = sy + shh // 2 - (30 if line else 0)
    paste_center(img, mark, sx + sw // 2, cy)
    if line:
        size_t = 48 if sw >= 1200 else 32
        text(d, (sx + sw // 2, cy + mark.height // 2 + 16), "Buy the world. Bankrupt your friends.", size_t, WHITE, anchor="ma")
    if pawns:
        picks = [14, 0, 15, 10, 3, 16, 12, 20, 7, 23, 11, 8, 1, 5, 9, 13, 2, 4, 6, 17, 18, 19, 21, 22, 24]
        k = 6 if h >= 600 else 4
        step = 20 * k + 12
        n = min(len(picks), w // step)
        x0 = (w - n * step) // 2
        for i in range(n):
            p = pawn(picks[i], k)
            img.alpha_composite(p, (x0 + i * step, h - p.height - max(10, h // 40)))
    img.convert("RGB").save(os.path.join(OUT, name))


def highlight(name, art):
    """An Instagram highlight cover: 1080 x 1920, art in the middle circle."""
    img = Image.new("RGBA", (1080, 1920), NIGHT + (255,))
    d = ImageDraw.Draw(img)
    d.ellipse((140, 560, 940, 1360), fill=FELT)
    d.ellipse((140, 560, 940, 1360), outline=GOLD, width=24)
    paste_center(img, art, 540, 960)
    img.convert("RGB").save(os.path.join(OUT, name))


def socials():
    for sub in ("youtube", "discord", "facebook", "tiktok", "reddit", "twitch", "instagram/highlights"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    # Profile pictures (one picture, every platform): circle-safe.
    for px, n in [(1080, "instagram/profile-1080.png"), (800, "youtube/avatar-800.png"), (512, "discord/server-icon-512.png"),
                  (720, "facebook/profile-720.png"), (1080, "tiktok/avatar-1080.png"), (256, "reddit/avatar-256.png"),
                  (800, "twitch/avatar-800.png")]:
        die_icon(px, FELT).convert("RGB").save(os.path.join(OUT, n))
    # Banners: each platform's size, content inside its safe area.
    banner((2560, 1440), "youtube/banner-2560x1440.png", 2, safe=(507, 508, 1546, 423))
    banner((1640, 624), "facebook/cover-1640x624.png", 1, safe=(150, 60, 1340, 504))
    banner((960, 540), "discord/banner-960x540.png", 1)
    banner((1920, 1080), "discord/invite-splash-1920x1080.png", 2)
    banner((1920, 384), "reddit/banner-1920x384.png", 1, line=False, pawns=False)
    banner((1200, 480), "twitch/offline-banner-1200x480.png", 1, line=True, pawns=False)
    banner((1500, 500), "x/header-1500x500.png", 1, safe=(0, 0, 1500, 420))
    # Highlight covers.
    em = up(load("emotes.png"), 24)
    house = up(load("house.png"), 14)
    cairo = city_strip(["cairo"], 11)[0]
    highlight("instagram/highlights/play.png", up(Image.open(f"{RAW}/die_5.png").convert("RGBA"), 3))
    highlight("instagram/highlights/pawns.png", pawn(14, 18))
    highlight("instagram/highlights/cities.png", cairo)
    highlight("instagram/highlights/chaos.png", em.crop((2 * 432, 0, 3 * 432, 432)))
    highlight("instagram/highlights/build.png", house)
    highlight("instagram/highlights/news.png", stacked(1, shadow=False))


def cities_post(size, name):
    """The board's cities: a grid of their property-card pictures."""
    img = backdrop(size, "table", 0.55)
    d = ImageDraw.Draw(img)
    w, h = size
    wide = w > h
    tag(img, (60, 56), "22 CITIES. ALL FOR SALE.", 32, GOLD)
    y = block(d, (60, 140), "Buy Paris. Build on Tokyo. Charge rent in Rio.", 64, w - 120, gap=1.15)
    names = ["cairo", "istanbul", "mumbai", "paris", "rome", "berlin", "tokyo", "sydney", "london", "new_york_city", "rio_de_janeiro", "hong_kong"]
    cols = 4 if wide else 3
    rows = 3 if wide else 4
    k = 6 if wide else 7
    pics = city_strip(names[: cols * rows], k)
    cw, ch = pics[0].width, pics[0].height
    gap = 20
    gw = cols * cw + (cols - 1) * gap
    x0 = (w - gw) // 2
    top = max(y + 40, (h - 100 - (rows * ch + (rows - 1) * gap)) // 2 + 50)
    for i, pic in enumerate(pics):
        x = x0 + (i % cols) * (cw + gap)
        yy = top + (i // cols) * (ch + gap)
        ImageDraw.Draw(img).rectangle((x - 6, yy - 6, x + cw + 5, yy + ch + 5), fill=INK)
        img.alpha_composite(pic, (x, yy))
    footer(img)
    img.convert("RGB").save(os.path.join(OUT, name))


def main():
    for sub in ("instagram", "x", "profile"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    sq, tall, story, wide = (1080, 1080), (1080, 1350), (1080, 1920), (1600, 900)
    announce(sq, "instagram/post-01-announce.png")
    toronto(tall, "instagram/post-02-toronto.png")
    pawns_post(tall, "instagram/post-03-pawns.png")
    chaos(tall, "instagram/post-04-chaos.png")
    screenshot_post(sq, "instagram/post-05-board.png", "board_table", "FORTY TILES. TWO DICE.", "One winner. Three former friends.")
    screenshot_post(sq, "instagram/post-06-locker.png", "locker", "THE LOCKER", "Dress for the rent you want.")
    story_announce(story, "instagram/story-01-announce.png")
    rules_story(story, "instagram/story-02-house-rules.png")

    announce(wide, "x/post-01-announce.png")
    toronto(wide, "x/post-02-toronto.png")
    pawns_post(wide, "x/post-03-pawns.png")
    chaos(wide, "x/post-04-chaos.png")
    avatar(400, "profile/avatar-400.png")
    avatar(800, "profile/avatar-800.png")
    cities_post(tall, "instagram/post-07-cities.png")
    cities_post(wide, "x/post-05-cities.png")
    logos()
    socials()   # (also the X header)

    # One download for the press page.
    zpath = os.path.join(OUT, "pixopoly-media-kit.zip")
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(OUT):
            for f in sorted(files):
                if f.endswith(".zip"):
                    continue
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, OUT))
    print("media kit built")


if __name__ == "__main__":
    main()
