# Mayada Mohamed Farhan: Digital Business Card

A single-page, no-build personal card (HTML + CSS + vanilla JS) meant to be opened from a QR code.

```
index.html          the card
qr.html             page with QR preview + PNG/SVG download buttons
css/style.css       all styling
js/script.js        contact settings (email / WhatsApp) + "Save contact"
assets/profile.jpg  YOUR PHOTO (add this file)
assets/favicon.svg
qr/                 mayada-card-qr.png and .svg
tools/make_qr.py    regenerate the QR if the URL ever changes
```

## 1. Before you deploy (2 minutes)
1. **Photo**: save a square, professional photo as `assets/profile.jpg` (about 400x400 px, under 150 KB). Until then, the card shows your initials.
2. **Contact**: open `js/script.js` and fill the two values at the top:
   ```js
   const CONFIG = { email: "you@example.com", whatsapp: "201001234567" };
   ```
   WhatsApp number: country code + number, digits only (Egypt: `20` + number without the leading 0).
   The "Let's connect" section stays hidden until at least one is filled.

## 2. Deploy on GitHub Pages
Use the repository name **`mayadafarhan.github.io`**. This gives the shortest, permanent URL: `https://mayadafarhan.github.io/`
1. On GitHub: **New repository**, name `mayadafarhan.github.io`, Public.
2. Upload all files from this folder (keep the folder structure), or:
   ```bash
   git init && git add . && git commit -m "Digital card"
   git branch -M main
   git remote add origin https://github.com/mayadafarhan/mayadafarhan.github.io.git
   git push -u origin main
   ```
3. Repo **Settings > Pages > Build and deployment**: Source = *Deploy from a branch*, Branch = `main`, folder `/ (root)`. Save.
4. Wait 1-2 minutes, then open `https://mayadafarhan.github.io/`.

Using a different repo name (e.g. `card`)? The URL becomes `https://mayadafarhan.github.io/card/`. Update the `canonical` and `og:` URLs in `index.html`, then run the QR step below.

## 3. QR code
`qr/mayada-card-qr.png` and `.svg` already point to `https://mayadafarhan.github.io/`. They stay valid as long as that URL does not change, and you can update the site any time without regenerating them.
Also available online at `https://mayadafarhan.github.io/qr.html` with download buttons.

To regenerate for another URL: `python tools/make_qr.py https://your-url/` (PNG needs `pip install pillow`).
Print tip: keep at least 2 cm size and the white border around the code.

## 4. Updating
Edit a file and push to `main`; Pages redeploys automatically. Your links (GitHub, portfolio, LinkedIn, CV) are in `index.html`.
CV: the Google Drive file must stay shared as "Anyone with the link" so visitors can view and download it.
