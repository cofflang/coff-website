#!/usr/bin/env python3
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
MOON = "https://cofflang.github.io/moonshot-website/"

GROUPS = [
    ("", [("", "home", "overview"), ("start", "start", "getting started"),
          ("releases", "releases", "releases")]),
    ("reference", [("language", "language", "the c0 language"),
                   ("compiler", "compiler", "the compiler"),
                   ("smed", "smed", "smed, assembler and linker")]),
]

def slug(text):
    t = re.sub(r"<[^>]+>", "", text)
    t = html.unescape(t).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t

def build(folder, name):
    raw = open(os.path.join(HERE, "pages", name + ".html")).read()
    title, desc, body = raw.split("\n", 2)
    prefix = "../" if folder else ""
    body = body.replace("{root}", prefix).replace("{moon}", MOON)
    sections = []
    n = [0]
    def h2(m):
        n[0] += 1
        text = m.group(1)
        sid = slug(text)
        sections.append((sid, text))
        return '<h2 id="%s"><span class="num">%d</span>%s</h2>' % (sid, n[0], text)
    if folder:
        body = re.sub(r"<h2>(.*?)</h2>", h2, body)
    toc = ['<ul class="toc">']
    for group, items in GROUPS:
        if group:
            toc.append('<li class="group">%s</li>' % group)
        for f, nm, label in items:
            href = prefix + (f + "/" if f else "") + "index.html"
            cur = ' aria-current="page"' if f == folder else ""
            toc.append('<li><a href="%s"%s>%s</a>' % (href, cur, label))
            toc.append("</li>")
    toc.append("</ul>")
    page_title = "coff" if not folder else "coff · " + title
    crumb = "" if not folder else '<p class="crumb"><a href="%sindex.html">coff</a> / %s</p>\n' % (prefix, folder)
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
<div class="frame">

<nav class="side" aria-label="contents">
<a class="brand" href="{prefix}index.html"><img src="{prefix}favicon.svg" alt="" width="28" height="28">coff</a>
{chr(10).join(toc)}
<p class="side-foot">written by <a href="https://tavro.se">tavro</a><br>part of <a href="{MOON}">moonshot</a><br>source on <a href="https://github.com/cofflang/coff">github</a></p>
</nav>

<main class="page">
{crumb}<h1>{title}</h1>
{body.strip()}
</main>

</div>
</body>
</html>
'''
    d = os.path.join(OUT, folder)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)

for group, items in GROUPS:
    for f, nm, label in items:
        build(f, nm)
print("written")
