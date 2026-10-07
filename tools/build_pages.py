"""Writes the plain pages (press kit, privacy, 404), which share a header and footer.

    python tools/build_pages.py
"""
import os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#171a2e">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icon-32.png">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
<header class="top">
  <a class="brand" href="/" aria-label="Pixopoly home">PIXOPOLY</a>
  <nav aria-label="Pages">
    <a href="/">Home</a>
    <a href="/presskit">Press kit</a>
    <a href="/privacy">Privacy</a>
  </nav>
  <a class="btn green sm" data-link="steam" href="/#wishlist">Wishlist</a>
</header>
"""


FOOT = """
<footer class="foot">
  <span class="brand">PIXOPOLY</span>
  <nav aria-label="More">
    <a href="/">Home</a>
    <a href="/presskit">Press kit</a>
    <a href="/privacy">Privacy</a>
    <a data-link="itch" href="https://intebat.itch.io/pixopoly" rel="noopener">itch.io</a>
  </nav>
  <small>&copy; <span id="year">2026</span> Pixopoly. Pixopoly is an independent game. It is not affiliated with, sponsored by or endorsed by Hasbro or the MONOPOLY brand. Steam and the Steam logo are trademarks of Valve Corporation.</small>
</footer>
<script src="/js/main.js" defer></script>
</body>
</html>
"""

SHOTS = ["board_table", "board_city", "board_map", "board_space", "deed", "trade", "manage", "locker", "menu", "results"]


def write(name, text):
    with open(os.path.join(SITE, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    grid = "\n".join(
        f'    <a class="shot" href="/assets/shots/{s}.webp" download>'
        f'<img src="/assets/shots/{s}_s.webp" alt="Screenshot: {s.replace("_", " ")}" width="960" height="540" loading="lazy"></a>'
        for s in SHOTS)
    write("presskit.html", head("Pixopoly press kit", "Facts, descriptions, screenshots and art for writing about Pixopoly.") + f"""
<main class="page">
  <h1>Press kit</h1>
  <p>Everything you need to write about Pixopoly. Use any of it. Screenshots are 1920 x 1080; click one to download it.</p>

  <section class="panel">
    <h2>Fact sheet</h2>
    <table>
      <tr><td>Game</td><td>Pixopoly</td></tr>
      <tr><td>Genre</td><td>Board game, strategy, party</td></tr>
      <tr><td>Players</td><td>2 to 6, any mix of people and CPUs (Easy, Normal, Hard)</td></tr>
      <tr><td>Modes</td><td>Online (Steam), on your network, hot-seat on one PC, 2 v 2 teams</td></tr>
      <tr><td>Platform</td><td>Windows PC (Steam)</td></tr>
      <tr><td>Release</td><td>Coming soon. No date announced.</td></tr>
      <tr><td>Price</td><td>To be announced</td></tr>
      <tr><td>Input</td><td>Mouse, keyboard, controller</td></tr>
      <tr><td>Prototype</td><td><a data-link="itch" href="https://intebat.itch.io/pixopoly" rel="noopener">Free build on itch.io</a></td></tr>
    </table>
  </section>

  <h2>One line</h2>
  <p>Buy the world. Bankrupt your friends.</p>
  <h2>One paragraph</h2>
  <p>Pixopoly is a pixel-art property trading board game for 2 to 6 players. Roll, buy, build and bankrupt your friends online, on your network or on one PC, with ability cards, chaos events and 2 v 2 teams on top of the rules everyone already knows.</p>
  <h2>The long version</h2>
  <p>Pixopoly takes the property trading board game everyone knows and rebuilds it as a fast, readable pixel-art game. The core is familiar: roll the dice, buy what you land on, complete colour sets, build houses and hotels, and collect rent until everyone else is broke. Properties you pass on go to auction, and anything can be traded.</p>
  <p>On top of that sits a sheet of house rules. Ability cards let you roll again, block a rent payment, halve a rival's income or take a house off their property. Chaos Mode draws a table-wide event every round, from market crashes to earthquakes. Four players can split into two teams that share colour sets and bail each other out.</p>
  <p>The table itself changes as you play: a town fills in around the board, a skyline rises as day turns to night, or a space station is assembled module by module. Pawns, dice, table cloths and titles unlock through play, levels and 54 achievements. There is no shop.</p>

  <h2>Features</h2>
  <ul>
    <li>Classic property trading rules with auctions, trading, mortgages, houses and hotels</li>
    <li>Online play through Steam with friend invites and six-letter codes</li>
    <li>Network play that works without Steam, and hot-seat play on one PC</li>
    <li>CPU players in three difficulties that trade, bid and build</li>
    <li>House rules: ability cards, Chaos Mode, 2 v 2 teams, landmarks, Sudden Death, extra ways to win</li>
    <li>Two boards: World Tour (22 cities) and Orbit</li>
    <li>Five tables that change over the course of a game</li>
    <li>25 pawns, 27 dice, 27 table cloths, 20 felt patterns and 54 achievements</li>
    <li>Controller support</li>
  </ul>

  <h2>Screenshots</h2>
  <div class="grid-shots">
{grid}
  </div>

  <h2>Logo, key art and social pictures</h2>
  <p><a href="/assets/img/og.png" download>Key art (1200 x 630)</a>. Scale pixel art up by whole numbers with nearest-neighbour filtering. Ready-made posts, banners and captions for Instagram and X are in the <a href="/media-kit/pixopoly-media-kit.zip" download>media kit (zip)</a>.</p>

  <h2>Credits</h2>
  <p>Font: Pixel Operator by Jayvee Enaguas, released under CC0.</p>
</main>
""" + FOOT)

    write("privacy.html", head("Pixopoly privacy", "What this website and the game do with your data: very little.") + """
<main class="page">
  <h1>Privacy</h1>
  <p>Last updated: 7 October 2026.</p>
  <h2>This website</h2>
  <p>This site sets no cookies, runs no analytics or advertising scripts, and has no forms. Fonts, images and scripts are served from this site, not from third parties.</p>
  <p>The company that hosts the site may keep standard server logs (such as IP address, browser type and time of request) to run and protect the service.</p>
  <h2>Links to other sites</h2>
  <p>Links to Steam, itch.io and other services take you to sites with their own privacy policies.</p>
  <h2>The game</h2>
  <p>The game stores your settings, saves and unlocks on your own computer. Online play uses Steam's networking and is covered by Valve's privacy policy. Network play sends data only between the computers in the game.</p>
  <h2>Changes</h2>
  <p>If this page changes, the date at the top changes with it.</p>
</main>
""" + FOOT)

    write("404.html", head("Pixopoly: nothing here", "This page doesn't exist.") + """
<main class="page" style="justify-items:center;text-align:center">
  <img src="/assets/img/die_1.png" alt="" width="134" height="134">
  <h1>You rolled a one.</h1>
  <p>There's nothing on this square. Go back to Payday and collect $200.</p>
  <p><a class="btn gold big" href="/">Back to the start</a></p>
</main>
""" + FOOT)
    print("pages built")


if __name__ == "__main__":
    main()
