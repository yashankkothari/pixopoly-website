"""Cuts the home page's pixel art (assets/px/) out of the game's own sprite sheets.
Needs the game repo at ~/Projects/pixonomy and Pillow. Run: python3 tools/build_px_art.py"""
import json, os, shutil, sys
from PIL import Image

GAME = os.path.expanduser("~/Projects/pixonomy/assets")
SPR = GAME + "/sprites"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "px")
os.makedirs(OUT, exist_ok=True)

RAMPS = {  # tools/art/lib.lua, dark -> light
    "red":    ["4f1230", "8c1f35", "c8323a", "ea5a47", "f99267"],
    "blue":   ["1a1c4a", "28398a", "3a66c8", "5c9ee8", "a5d6f7"],
    "green":  ["123a3a", "1f6b45", "3c9a4a", "78c452", "bfe37a"],
    "yellow": ["8a5a14", "c98f1e", "f0c62e", "fbe36a", "fff6b5"],
    "purple": ["2a1247", "4f2382", "7c42c0", "a877e0", "d6b6f5"],
    "teal":   ["123048", "1b5a66", "2a8f8a", "5cc7ac", "b3ecd0"],
    "orange": ["7a2a1e", "b54a22", "e87a2c", "f8a94a", "fdd583"],
    "pink":   ["5c1a4f", "9c2f6e", "d4548f", "f08ab0", "fbc6d2"],
}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def save(im, name):
    im.save(f"{OUT}/{name}", optimize=True)
    print(name, im.size)


# Logo: the letter sheet laid out as one word.
lj = json.load(open(SPR + "/logo.json"))
lsheet = Image.open(SPR + "/logo.png").convert("RGBA")
word, gap = "PIXONOMY", 4
w = sum(lj[c][2] for c in word) + gap * (len(word) - 1)
logo = Image.new("RGBA", (w, max(lj[c][3] for c in word)))
x = 0
for c in word:
    lx, ly, lw, lh = lj[c]
    logo.alpha_composite(lsheet.crop((lx, ly, lx + lw, ly + lh)), (x, 0))
    x += lw + gap
save(logo, "logo.png")

# Pawns: every piece, recoloured from the key ramp, six frames per row.
pj = json.load(open(SPR + "/pawns.json"))
psheet = Image.open(SPR + "/pawns.png").convert("RGBA")
kinds = ["Cat", "Duck", "Robot", "Ghost", "Dino", "Car", "Frog", "Penguin", "Rocket", "Crown", "Dog",
         "Piggy Bank", "Boat", "Castle", "Alien", "UFO", "Mushroom", "Slime", "Crab", "Pumpkin", "Teapot",
         "Cactus", "Boot", "Skateboard", "Moneybag", "Trophy", "Pawn"]
cols = ["red", "yellow", "blue", "purple", "green", "orange", "teal", "pink"]
strip = Image.new("RGBA", (20 * 6, 24 * len(kinds)))
for r, k in enumerate(kinds):
    ramp = [rgb(h) for h in RAMPS[cols[r % len(cols)]]]
    for f in range(6):
        fx, fy, fw, fh = pj[f"{k}_{f}"]
        cell = psheet.crop((fx, fy, fx + fw, fy + fh))
        px = cell.load()
        for yy in range(fh):
            for xx in range(fw):
                pr, pg, pb, pa = px[xx, yy]
                if pa and pr == 255 and pg == 0 and 160 <= pb <= 224:
                    px[xx, yy] = ramp[(pb - 160) // 16] + (pa,)
        strip.alpha_composite(cell, (f * 20, r * 24))
save(strip, "pawns.png")

# Dice: twelve tumble frames, then a resting die per top face 1..6.
dj = json.load(open(SPR + "/dice/classic.json"))
dsheet = Image.open(SPR + "/dice/classic.png").convert("RGBA")
names = [f"32_tumble{i}" for i in range(12)] + [next(k for k in dj if k.startswith(f"32_{v}") and "tumble" not in k) for v in range(1, 7)]
dice = Image.new("RGBA", (66 * len(names), 66))
for i, n in enumerate(names):
    x0, y0, w0, h0 = dj[n]
    dice.alpha_composite(dsheet.crop((x0, y0, x0 + w0, y0 + h0)), (i * 66, 0))
save(dice, "dice.png")
print("dice faces:", names[12:])

# Tile art for the 36 World Tour tiles (in board order), one strip, 88x108 cells.
TILES = ["payday_c", "rail0_p", "cairo", "istanbul", "mail_p", "mumbai", "bangkok", "tax_p", "rio_de_janeiro",
         "lockup_c", "mexico_city", "athens", "power_p", "rail1_p", "toronto", "wild_p", "tel_aviv", "seoul",
         "loan_c", "rail2_p", "los_angeles", "paris", "mail_p", "rome", "berlin", "water_p", "dubai", "spin_c",
         "tokyo", "sydney", "wild_p", "rail3_p", "hong_kong", "london", "lux_p", "new_york_city"]
CW, CH = 88, 88
tiles = Image.new("RGBA", (CW * len(TILES), CH))
for i, t in enumerate(TILES):
    p = f"{SPR}/cities/36_hd/{t}.png"
    if not os.path.exists(p):
        p = f"{SPR}/specials36_hd/{t}.png"
    im = Image.open(p).convert("RGBA")
    l, t = (im.width - CW) // 2, (im.height - CH) // 2   # centre square, whole pixels
    im = im.crop((l, t, l + CW, t + CH))
    tiles.alpha_composite(im, (i * CW, 0))
save(tiles, "tiles.png")

# Single city scenes for the deed cards.
for c in ["istanbul", "tokyo", "paris", "new_york_city", "london", "rio_de_janeiro", "dubai", "seoul", "sydney", "cairo"]:
    save(Image.open(f"{SPR}/cities/36_hd/{c}.png").convert("RGBA"), f"city-{c.replace('_', '-')}.png")

# Board pictures (the tilted view only for World Tour) and the splash.
for b in ["classic", "orbit", "states", "euro"]:
    shutil.copy(f"{GAME}/previews/board_{b}_full.png", f"{OUT}/board-{b}.png")
shutil.copy(f"{GAME}/previews/board_classic_tilt.png", f"{OUT}/board-classic-tilt.png")
shutil.copy(f"{GAME}/brand/splash.png", f"{OUT}/splash.png")
Image.open(SPR + "/tables/table.png").convert("RGB").save(f"{OUT}/table.webp", quality=88)
print("done")

# Share card (1200x630) and icons.
from PIL import ImageFont, ImageDraw
og = Image.open(SPR + "/tables/table.png").convert("RGBA").crop((0, 0, 1160, 630)).resize((1200, 630), Image.NEAREST)
tilt = Image.open(f"{GAME}/previews/board_classic_tilt.png").convert("RGBA")
tilt = tilt.resize((int(tilt.width * 1.3), int(tilt.height * 1.3)), Image.LANCZOS)
og.alpha_composite(tilt, ((1200 - tilt.width) // 2, 630 - tilt.height + 120))
shade = Image.new("RGBA", (1200, 300), (20, 16, 26, 0))
sd = ImageDraw.Draw(shade)
for y in range(300):
    sd.line([(0, y), (1200, y)], fill=(20, 16, 26, int(215 * (1 - y / 300))))
og.alpha_composite(shade, (0, 0))
lg = logo.resize((logo.width * 2, logo.height * 2), Image.NEAREST)
sh = Image.new("RGBA", lg.size, (20, 16, 26, 255)); sh.putalpha(lg.getchannel("A"))
og.alpha_composite(sh, ((1200 - lg.width) // 2, 48 + 10))
og.alpha_composite(lg, ((1200 - lg.width) // 2, 48))
font = ImageFont.truetype(GAME + "/fonts/PixonomyHead.ttf", 48)
d = ImageDraw.Draw(og)
t = "THE PROPERTY TRADING BOARD GAME"
tw = d.textlength(t, font=font)
d.text(((1200 - tw) // 2, 48 + lg.height + 22 + 4), t, font=font, fill=(20, 16, 26))
d.text(((1200 - tw) // 2, 48 + lg.height + 22), t, font=font, fill=(253, 247, 227))
og.convert("RGB").save(f"{OUT}/og.png", optimize=True)
icon = Image.open(f"{GAME}/brand/app_icon.png").convert("RGBA")
for n in (32, 180):
    icon.resize((n, n), Image.LANCZOS if icon.width > n * 2 else Image.NEAREST).save(f"{OUT}/icon-{n}.png", optimize=True)
print("og + icons", icon.size)
