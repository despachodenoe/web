#!/usr/bin/env python3
"""
Despacho de Noé — Build Script
Converts Markdown posts in _posts/ to HTML in posts/
Also regenerates index.html with latest posts.
"""

import os
import json
import math
import shutil
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
MD_EXTENSIONS = ['extra', 'codehilite', 'toc', 'smarty']

CATEGORY_LABELS = {
    "opiniones":       "Opiniones",
    "recomendaciones": "Recomendaciones",
    "historias":       "Historias",
    "conversaciones":  "Conversaciones",
}

def reading_time(text: str) -> int:
    words = len(text.split())
    return max(1, math.ceil(words / 200))

def format_date(date_str: str) -> str:
    MONTHS = {
        1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",
        7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"
    }
    try:
        d = datetime.strptime(str(date_str), "%Y-%m-%d")
        return f"{d.day} de {MONTHS[d.month]}, {d.year}"
    except Exception:
        return str(date_str)

def slug_from_filename(path: Path) -> str:
    name = path.stem
    # Strip date prefix if present: 2025-01-15-titulo → titulo
    parts = name.split("-")
    if len(parts) > 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        return "-".join(parts[3:])
    return name

def build_posts():
    OUTPUT_DIR.mkdir(exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)

    post_template = env.get_template("post.html")
    index_template = env.get_template("index.html")

    all_posts = []

    md_files = sorted(POSTS_DIR.rglob("*.md"), reverse=True)

    for md_file in md_files:
        post = frontmatter.load(md_file)
        meta = post.metadata

        # Required fields with sensible defaults
        title    = meta.get("title", md_file.stem.replace("-", " ").title())
        category = meta.get("category", "opiniones").lower()
        date_raw = meta.get("date", datetime.today().strftime("%Y-%m-%d"))
        excerpt  = meta.get("excerpt", "")
        slug     = meta.get("slug", slug_from_filename(md_file))
        author   = meta.get("author", "Noé")
        draft    = meta.get("draft", False)

        if draft:
            print(f"  ↷ Skipping draft: {md_file.name}")
            continue

        body_md  = post.content
        body_html = markdown.markdown(body_md, extensions=MD_EXTENSIONS)
        read_min = reading_time(body_md)
        date_fmt = format_date(date_raw)
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
            "url":       f"posts/{slug}.html",
            "body":      body_html,
        }

        # Render post HTML
        output_path = OUTPUT_DIR / f"{slug}.html"
        rendered = post_template.render(**post_data)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"  ✓ Built: {output_path}")

        all_posts.append(post_data)

    # Sort posts by date descending
    all_posts.sort(key=lambda p: p["date_raw"], reverse=True)

    # Render index
    index_path = ROOT_DIR / "index.html"
    rendered_index = index_template.render(
        posts=all_posts,
        posts_json=json.dumps([{k: v for k, v in p.items() if k != "body"} for p in all_posts]),
        featured=all_posts[0] if all_posts else None,
        recent=all_posts[1:POSTS_PER_PAGE] if len(all_posts) > 1 else [],
    )
    index_path.write_text(rendered_index, encoding="utf-8")
    print(f"  ✓ Rebuilt: index.html ({len(all_posts)} posts)")

    return all_posts

if __name__ == "__main__":
    print("🏛  Despacho de Noé — Building blog...\n")
    posts = build_posts()
    print(f"\n✅  Done. {len(posts)} posts generated.")
