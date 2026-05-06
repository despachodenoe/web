usr/bin/env python3
"""
Despacho de Noé — Build Script
Converts .md posts in _posts/ to HTML in posts/.
Filenames come straight from the .md filename (no date prefix required).
All metadata is read from the frontmatter.
Supports: title, category, date, excerpt, author, slug, image, draft, tags.
"""

import os
import re
import json
import math
import frontmatter
import markdown
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# ── Config ──────────────────────────────────────
POSTS_DIR     = Path("_posts")
OUTPUT_DIR    = Path("posts")
TEMPLATES_DIR = Path("_templates")
ROOT_DIR      = Path(".")
POSTS_PER_PAGE = 9

MD_EXTENSIONS = ['extra', 'codehilite', 'toc', 'smarty', 'nl2br']

CATEGORY_LABELS = {
    "opiniones":       "Opiniones",
    "recomendaciones": "Recomendaciones",
    "historias":       "Historias",
    "conversaciones":  "Conversaciones",
}

MONTHS_ES = {
    1:"enero", 2:"febrero", 3:"marzo", 4:"abril",
    5:"mayo", 6:"junio", 7:"julio", 8:"agosto",
    9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"
}

def reading_time(text: str) -> int:
    words = len(text.split())
    return max(1, math.ceil(words / 200))

def format_date(date_val) -> str:
    try:
        if isinstance(date_val, str):
            d = datetime.strptime(date_val.strip(), "%Y-%m-%d")
        else:
            d = date_val  # already a date/datetime object
        return f"{d.day} de {MONTHS_ES[d.month]}, {d.year}"
    except Exception:
        return str(date_val)

def slug_from_path(path: Path) -> str:
    """
    Use the filename as slug directly.
    Strips optional YYYY-MM-DD- prefix if present for backward compat.
    despacho-para-siempre.md  → despacho-para-siempre
    2025-01-15-mi-articulo.md → mi-articulo  (legacy support)
    """
    name = path.stem
    legacy = re.match(r'^\d{4}-\d{2}-\d{2}-(.+)$', name)
    if legacy:
        return legacy.group(1)
    return name

def find_related(current: dict, all_posts: list, n: int = 3) -> list:
    """Return up to n posts in the same category, excluding current."""
    same_cat = [p for p in all_posts
                if p["slug"] != current["slug"] and p["category"] == current["category"]]
    # Fill remaining slots with other posts if needed
    others = [p for p in all_posts
              if p["slug"] != current["slug"] and p["category"] != current["category"]]
    pool = (same_cat + others)[:n]
    return pool

def build_posts():
    OUTPUT_DIR.mkdir(exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)
    post_tpl  = env.get_template("post.html")
    index_tpl = env.get_template("index.html")

    all_posts = []

    for md_file in sorted(POSTS_DIR.rglob("*.md"), reverse=True):
        post = frontmatter.load(md_file)
        meta = post.metadata

        # ── Read all frontmatter fields ──
        title    = meta.get("title", md_file.stem.replace("-", " ").title())
        category = str(meta.get("category", "opiniones")).lower().strip()
        date_raw = meta.get("date", datetime.today().strftime("%Y-%m-%d"))
        excerpt  = meta.get("excerpt", "")
        author   = meta.get("author", "Noé")
        draft    = meta.get("draft", False)
        tags     = meta.get("tags", [])
        image    = meta.get("image", "")   # e.g. "assets/images/mi-foto.jpg" or a URL

        # slug: prefer explicit, else derive from filename
        slug = meta.get("slug") or slug_from_path(md_file)

        if draft:
            print(f"  ↷  Skipping draft: {md_file.name}")
            continue

        body_md   = post.content
        body_html = markdown.markdown(body_md, extensions=MD_EXTENSIONS)
        read_min  = reading_time(body_md)
        date_fmt  = format_date(date_raw)
        cat_label = CATEGORY_LABELS.get(category, category.capitalize())

        post_data = {
            "title":     title,
            "category":  category,
            "cat_label": cat_label,
            "date_raw":  str(date_raw),
            "date":      date_fmt,
            "excerpt":   excerpt,
            "slug":      slug,
            "author":    author,
            "read_min":  read_min,
            "tags":      tags,
            "image":     image,           # passed to template
            "url":       f"posts/{slug}.html",
            "body":      body_html,
        }

        all_posts.append(post_data)

    # Sort by date descending
    all_posts.sort(key=lambda p: p["date_raw"], reverse=True)

    # Render each post (needs related posts, so do after collecting all)
    for post_data in all_posts:
        related = find_related(post_data, all_posts, n=3)
        output_path = OUTPUT_DIR / f"{post_data['slug']}.html"
        rendered = post_tpl.render(**post_data, related_posts=related)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"  ✓  {output_path}  [{post_data['cat_label']}]")

    # Render index
    # Strip body from JSON (too heavy), keep everything else
    posts_json = json.dumps([
        {k: v for k, v in p.items() if k != "body"}
        for p in all_posts
    ], ensure_ascii=False)

    featured = all_posts[0] if all_posts else None
    recent   = all_posts[1:POSTS_PER_PAGE] if len(all_posts) > 1 else []

    index_html = index_tpl.render(
        posts=all_posts,
        posts_json=posts_json,
        featured=featured,
        recent=recent,
    )
    (ROOT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"\n  ✓  index.html  ({len(all_posts)} artículos)")

    return all_posts

if __name__ == "__main__":
    print("\n🏛  Despacho de Noé — Building blog...\n")
    posts = build_posts()
    print(f"\n✅  Listo. {len(posts)} artículos generados.\n")
