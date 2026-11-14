#!/usr/bin/env python3
"""Rebuild feed.xml (Atom) from the posts in news.html.

Run from the repo root after adding a post:  python3 scripts/build-feed.py
Standard library only. news.html is the source of truth; never edit feed.xml by hand.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://boredsoftware.space"
src = (ROOT / "news.html").read_text(encoding="utf-8")

posts = re.findall(
    r'<article id="([^"]+)">.*?<time datetime="([^"]+)">.*?<span class="chip [^"]+">([^<]+)</span>'
    r'.*?<h2><a [^>]*>(.*?)</a></h2>(.*?)</div>\s*</article>',
    src, flags=re.S)
if not posts:
    raise SystemExit("No posts found in news.html")


def absolute(body):
    """Make relative links absolute so they work in feed readers."""
    def fix(m):
        url = m.group(2)
        if url.startswith("#"):
            url = f"{SITE}/news.html{url}"
        elif not re.match(r"^(https?:|mailto:)", url):
            url = f"{SITE}/{url.lstrip('./')}"
        return f'{m.group(1)}"{url}"'
    return re.sub(r'(href=)"([^"]+)"', fix, body)


entries = []
for pid, date, app, title, body in posts:
    body = re.sub(r"\s+", " ", absolute(body)).strip()
    entries.append(f"""  <entry>
    <id>{SITE}/news.html#{pid}</id>
    <title>{html.escape(html.unescape(title))}</title>
    <link href="{SITE}/news.html#{pid}"/>
    <updated>{date}T12:00:00-08:00</updated>
    <category term="{html.escape(app)}"/>
    <content type="html">{html.escape(body)}</content>
  </entry>""")

feed = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Bored Software news</title>
  <subtitle>Releases and updates for Bored Room, Bored Scanner, Bored Package and Bored Guest.</subtitle>
  <id>{SITE}/news.html</id>
  <link href="{SITE}/news.html"/>
  <link rel="self" href="{SITE}/feed.xml"/>
  <updated>{posts[0][1]}T12:00:00-08:00</updated>
  <author><name>Bored Software</name></author>
  <icon>{SITE}/favicon.png</icon>
{chr(10).join(entries)}
</feed>
"""
(ROOT / "feed.xml").write_text(feed, encoding="utf-8")
print(f"feed.xml: {len(posts)} posts, newest {posts[0][1]} {posts[0][3]}")
