# boredsoftware.space

Landing page for Bored Software: Bored Room, Bored Scanner, Bored Package and Bored Guest.
Static HTML and one `style.css`. No build step, no JavaScript, no analytics.
Served by GitHub Pages from `main`. App icons are copies of each app site's `apple-touch-icon.png`.

## Fonts and Content-Security-Policy

Instrument Sans is self-hosted in `fonts/` (`@font-face` at the top of `style.css`, licence in `fonts/OFL.txt`); the site makes no third-party requests. Every page has a `Content-Security-Policy` meta tag (`default-src 'self'`, no scripts), so inline `style=` attributes and `<style>` blocks are blocked: add a class in `style.css` instead (one-off tweaks are the `u-` classes at the bottom). New pages need the same meta tag.
