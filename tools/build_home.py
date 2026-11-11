"""Builds index.html (the home page) from tools/home.src.html: fills in the FAQ, the structured
data, the pawn parade and the board ticker. Run: python3 tools/build_home.py"""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = "https://pixopoly-website.vercel.app"
URL = SITE + "/"
ITCH = "https://intebat.itch.io/pixonomy"

DESC = ("Pixonomy is a pixel-art property trading board game for 2 to 6 players on PC. Roll the dice, buy cities, "
        "build houses and hotels, collect rent, trade and bid at auction until one tycoon is left. "
        "Play online with Steam friends, over LAN, on one PC or against CPU rivals. The prototype is free on itch.io.")

FAQ = [
    ("What kind of game is Pixonomy?",
     "Pixonomy is a property trading board game in pixel art. You roll two dice, move round a board of 36 tiles, "
     "buy the cities you land on, complete colour sets, build houses and hotels, and collect rent from everyone who "
     "lands on your property. Trade, bid at auctions and bluff your way to the top: the last player with money wins."),
    ("Can I play Pixonomy online with friends?",
     "Yes. Invite your Steam friends to play online, host a game on your local network (LAN), or share one PC and "
     "pass the mouse or controller round. You can fill any empty seat with a CPU player."),
    ("How many players can play?",
     "2 to 6 players, in any mix of people and computer players."),
    ("Can I play alone against the computer?",
     "Yes. CPU rivals come in Easy, Normal and Hard, and they trade, bid at auctions and build just like people do. "
     "There's also a daily challenge with the same dice and cards for every player."),
    ("If I know the classic property board game, will I know how to play?",
     "Yes. Roll, buy, build, collect rent and bankrupt your rivals: the core loop is the one you know from the kitchen "
     "table. Pixonomy adds a deal slip with promises and IOUs, auctions, a Bank Loan corner, the Lucky Spin, ability "
     "cards, Chaos Mode, secret missions, teams and underdog rules, all of which you can switch on or off."),
    ("How long does a game take?",
     "You choose. Set a round limit and the richest player wins when the rounds run out, pick the Quick preset for a "
     "short game, or play the classic way until only one player is left."),
    ("Does Pixonomy have house rules like auctions and a jackpot?",
     "Yes. Auctions and even building are on by default. You can also set the starting cash, a round limit, a turn "
     "timer and a jackpot that pays out on the Lucky Spin, turn on teams, ability cards and Chaos Mode, or add extra "
     "ways to win by sets, cash or railroads."),
    ("Can I play Pixonomy for free?",
     "Yes. A free prototype is on itch.io right now, so you can roll the dice and buy your first city today. "
     "The full game is coming to Steam."),
    ("Which platforms is Pixonomy on?",
     "Pixonomy is coming to Steam for Windows PC. You can play with a mouse, a keyboard or a controller."),
    ("When does Pixonomy come out?",
     "Pixonomy is in development and has no release date yet. Wishlist it on Steam and Steam will tell you the day it "
     "comes out; until then, the free prototype is on itch.io."),
]

PAWNS = ["Cat", "Duck", "Robot", "Ghost", "Dino", "Car", "Frog", "Penguin", "Rocket", "Crown", "Dog",
         "Piggy Bank", "Boat", "Castle", "Alien", "UFO", "Mushroom", "Slime", "Crab", "Pumpkin", "Teapot",
         "Cactus", "Boot", "Skateboard", "Moneybag", "Trophy", "Pawn"]

SHOTS = [f"{SITE}/assets/shots/{n}.webp" for n in ("board_table", "deed", "trade", "board_city", "board_space", "board_map", "manage")]

LD = [
    {"@context": "https://schema.org", "@type": "VideoGame", "@id": URL + "#game", "name": "Pixonomy",
     "url": URL, "description": DESC, "image": SITE + "/assets/px/og.png", "screenshot": SHOTS,
     "trailer": {"@type": "VideoObject", "name": "Pixonomy teaser", "description": "Dice, pawns and houses on the Pixonomy board.",
                 "contentUrl": SITE + "/assets/video/reel.mp4", "thumbnailUrl": SITE + "/assets/video/teaser_poster.jpg",
                 "uploadDate": "2026-11-11"},
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "url": ITCH, "name": "Free prototype on itch.io",
                "availability": "https://schema.org/InStock"},
     "genre": ["Board game", "Strategy", "Party", "Trading", "Economic simulation"],
     "keywords": "property trading board game, board game online with friends, dice board game, real estate board game, "
                 "pixel art board game, local multiplayer board game, hot-seat board game, tycoon board game, family board game",
     "gamePlatform": ["PC", "Windows", "Steam"], "operatingSystem": "Windows",
     "applicationCategory": "Game", "playMode": ["SinglePlayer", "MultiPlayer"],
     "numberOfPlayers": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 6},
     "inLanguage": "en", "sameAs": [ITCH]},
    {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "name": "Pixonomy", "url": URL},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]


def build():
    src = open(os.path.join(HERE, "home.src.html"), encoding="utf-8").read()
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in LD)
    faq = "".join(f'<details class="slab paper"><summary>{html.escape(q)}</summary><div class="a"><p>{html.escape(a)}</p></div></details>'
                  for q, a in FAQ)
    parade = "".join(f'<button type="button"><span class="pawn idle" style="--r:{i}"></span>{html.escape(n)}</button>'
                     for i, n in enumerate(PAWNS))
    ticker = "".join(f'<i style="--t:{i % 36}"></i>' for i in range(72))  # twice round, so the loop is seamless
    out = (src.replace("<!--LD-->", ld.rstrip()).replace("<!--FAQ-->", faq)
           .replace("<!--PARADE-->", parade).replace("<!--TICKER-->", ticker))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out.replace("<!doctype html>\n", "<!doctype html>\n<!-- Generated by tools/build_home.py from tools/home.src.html. Edit those, not this. -->\n", 1))
    print("built index.html")


if __name__ == "__main__":
    build()
