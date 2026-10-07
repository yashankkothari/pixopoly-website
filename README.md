# Pixopoly website

The marketing site for Pixopoly. Plain HTML, CSS and JavaScript: no build step, no dependencies.

## Put it on Vercel

1. Push this folder to a GitHub repository (see below).
2. On vercel.com choose **Add New > Project** and import the repository.
3. Leave every setting as it is (Framework Preset: **Other**, no build command, output directory empty) and press **Deploy**.

Or from this folder with the Vercel CLI: `npx vercel` for a preview, `npx vercel --prod` to go live.

`vercel.json` already sets clean URLs (`/presskit`, `/privacy`), security headers and caching. `404.html` is served for unknown addresses automatically.

### First push to GitHub

```
git remote add origin https://github.com/<you>/pixopoly-website.git
git push -u origin main
```

## When the Steam page exists

Open `js/main.js` and fill in `CONFIG.steam`. Every "Wishlist" button becomes a real link; until then they say "Steam page soon".

## What's where

| Path | What it is |
|---|---|
| `index.html` | The whole home page |
| `css/style.css`, `js/main.js` | Look and behaviour |
| `presskit.html`, `privacy.html`, `404.html` | Written by `tools/build_pages.py` (shared header and footer) |
| `assets/img`, `assets/shots` | Art and screenshots, built by `tools/build_assets.py` from the game |
| `assets/fonts` | Pixel Operator Bold (CC0) |
| `media-kit/` | Posts, banners and captions for Instagram and X (`tools/build_media_kit.py`) |
| `vercel.json` | Hosting settings |

## Rebuilding the art

The images come from the game project. After the game's art changes:

```
python tools/build_assets.py      # sprites, logo, icons, screenshots, share picture
python tools/build_pages.py       # press kit, privacy, 404
python tools/build_media_kit.py   # social pictures and the zip
```

`build_assets.py` reads three folders, set with environment variables if they move:
`PIXOPOLY_GAME` (the Godot project), `PIXOPOLY_RAW` (dice, pawns and table art exported from the game) and `PIXOPOLY_SHOTS` (1920x1080 screenshots).

## Preview on your own machine

```
python -m http.server 8000
```

Then open http://localhost:8000.
