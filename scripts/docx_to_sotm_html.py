#!/usr/bin/env python3
"""Convert Smoke on the Mediterranean publication docx to chapter HTML.

Preserves user wording. Puts Sources (and glossary / names appendices) in
collapsed <details> blocks. Extracts inline images next to their paragraphs.
"""
from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

STYLE = """
  :root { color-scheme: dark; }
  body { margin:0; background:#1c1814; color:#ede4d4; font-family: Palatino, Georgia, serif; }
  main { max-width: 42rem; margin: 0 auto; padding: 1.5rem 1.2rem 3.5rem; }
  a { color:#e7c7a4; }
  .nav { font-size: 0.9rem; margin-bottom: 1.2rem; }
  .chapternum { color:#c4b49a; letter-spacing: 0.08em; font-size: 0.8rem; text-transform: uppercase; }
  h1 { font-weight: 600; letter-spacing: 0.03em; font-size: 1.7rem; margin: 0.35rem 0 0.4rem; line-height: 1.2; }
  .dek { color:#c4b49a; font-style: italic; margin: 0 0 1.6rem; line-height: 1.4; }
  p { line-height: 1.55; margin: 0 0 0.95rem; }
  .break { text-align: center; color:#8a7a66; letter-spacing: 0.35em; margin: 1.6rem 0; }
  figure { margin: 1.4rem 0; }
  figure img { width: 100%; height: auto; display: block; border-radius: 2px; }
  figcaption { font-size: 0.8rem; color:#a89984; margin-top: 0.4rem; }
  details.back { margin-top: 2rem; border-top: 1px solid #3a3228; padding-top: 0.8rem; }
  details.back + details.back { margin-top: 0.6rem; border-top: none; padding-top: 0; }
  summary { cursor: pointer; color:#e7c7a4; font-weight: 600; letter-spacing: 0.04em; list-style: none; }
  summary::-webkit-details-marker { display: none; }
  summary::before { content: "▸ "; color:#8a7a66; }
  details[open] summary::before { content: "▾ "; }
  .back ul { padding-left: 1.1rem; margin: 0.6rem 0 0; }
  .back li { margin: 0.35rem 0; line-height: 1.45; }
  .rtl { direction: rtl; unicode-bidi: plaintext; }
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def blip_embeds(paragraph) -> list[str]:
    out = []
    for blip in paragraph._p.xpath('.//*[local-name()="blip"]'):
        rid = blip.get(f"{REL_NS}embed")
        if rid:
            out.append(rid)
    return out


def classify_tail(text: str) -> str | None:
    t = text.strip()
    if re.match(r"^Sources\b", t, re.I):
        return "sources"
    if re.search(r"Mini-Glossary\s*$", t) or re.search(r"\bMini-Glossary\b", t):
        return "glossary"
    if re.search(r"Appendix of Important Names", t, re.I):
        return "names"
    return None


def is_bullet(text: str) -> bool:
    return text.lstrip().startswith("•") or text.lstrip().startswith("- ")


def bullet_html(text: str) -> str:
    t = text.lstrip()
    if t.startswith("•"):
        t = t[1:].strip()
    elif t.startswith("- "):
        t = t[2:].strip()
    return f"<li>{esc(t)}</li>"


def extract_images(docx_path: Path, out_img_dir: Path, stem: str) -> dict[str, str]:
    """Map relationship id -> relative web path for extracted media."""
    out_img_dir.mkdir(parents=True, exist_ok=True)
    mapping: dict[str, str] = {}
    doc = Document(str(docx_path))
    rels = doc.part.rels
    # Collect rIds that are images in document order for stable numbering
    order: list[str] = []
    for p in doc.paragraphs:
        for rid in blip_embeds(p):
            if rid not in order:
                order.append(rid)
    with zipfile.ZipFile(docx_path) as z:
        for n, rid in enumerate(order, start=1):
            rel = rels.get(rid)
            if rel is None:
                continue
            target = rel.target_ref  # e.g. media/image1.jpg
            zip_name = "word/" + target.lstrip("/")
            if zip_name not in z.namelist():
                # sometimes target is ../media/
                zip_name = "word/media/" + Path(target).name
            if zip_name not in z.namelist():
                continue
            ext = Path(zip_name).suffix.lower() or ".jpg"
            fname = f"{stem}-img{n:02d}{ext}"
            data = z.read(zip_name)
            (out_img_dir / fname).write_bytes(data)
            mapping[rid] = f"images/{fname}"
    return mapping


def convert_one(docx_path: Path, out_dir: Path) -> Path:
    stem = docx_path.stem  # sotm0005-eg-en
    m = re.match(r"sotm(\d{4})-([a-z]{2})-([a-z]{2})$", stem)
    lang = m.group(3) if m else "en"
    rtl = lang in {"ar", "he"}

    img_map = extract_images(docx_path, out_dir / "images", stem)
    doc = Document(str(docx_path))

    chapter_num = ""
    title = ""
    dek = ""
    body_html: list[str] = []
    section = "front"  # front | body | glossary | names | sources
    section_items: dict[str, list[str]] = {"glossary": [], "names": [], "sources": []}
    front_texts: list[str] = []

    def flush_front():
        nonlocal chapter_num, title, dek
        texts = [t for t in front_texts if t]
        if not texts:
            return
        if re.match(r"^Chapter\s+\d+", texts[0], re.I):
            chapter_num = texts[0]
            texts = texts[1:]
        if texts:
            title = texts[0]
            texts = texts[1:]
        if texts:
            dek = texts[0]

    for p in doc.paragraphs:
        embeds = blip_embeds(p)
        text = (p.text or "").strip()

        if embeds:
            if section == "front":
                flush_front()
                section = "body"
            for rid in embeds:
                src = img_map.get(rid)
                if not src:
                    continue
                body_html.append(
                    f'<figure><img src="{esc(src)}" alt="" loading="lazy"></figure>'
                )
            if not text:
                continue

        if not text:
            continue

        marker = classify_tail(text)
        if marker:
            if section == "front":
                flush_front()
            section = marker
            continue

        if section == "front":
            # scene break before we got title block complete still front
            if text == "* * *":
                flush_front()
                section = "body"
                body_html.append('<p class="break">* * *</p>')
            else:
                front_texts.append(text)
                # after 3 front lines, rest is body
                if len(front_texts) >= 3:
                    flush_front()
                    section = "body"
            continue

        if section in {"glossary", "names", "sources"}:
            if is_bullet(text):
                section_items[section].append(bullet_html(text))
            else:
                section_items[section].append(f"<li>{esc(text)}</li>")
            continue

        # body
        if text == "* * *":
            body_html.append('<p class="break">* * *</p>')
        else:
            body_html.append(f"<p>{esc(text)}</p>")

    if section == "front":
        flush_front()

    rtl_attr = ' class="rtl"' if rtl else ""
    lang_attr = esc(lang)

    parts = [
        "<!DOCTYPE html>",
        f'<html lang="{lang_attr}">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(title or stem)} — Smoke on the Mediterranean</title>",
        f"<style>{STYLE}</style>",
        "</head>",
        f"<body{rtl_attr}>",
        "<main>",
        '<p class="nav"><a href="index.html">Smoke on the Mediterranean</a></p>',
    ]
    if chapter_num:
        parts.append(f'<p class="chapternum">{esc(chapter_num)}</p>')
    if title:
        parts.append(f"<h1>{esc(title)}</h1>")
    if dek:
        parts.append(f'<p class="dek">{esc(dek)}</p>')
    parts.extend(body_html)

    labels = {
        "glossary": "Mini-glossary",
        "names": "Important names",
        "sources": "Sources",
    }
    # Sources last; glossary and names before it
    for key in ("glossary", "names", "sources"):
        items = section_items[key]
        if not items:
            continue
        parts.append(f'<details class="back"><summary>{labels[key]}</summary>')
        parts.append("<ul>")
        parts.extend(items)
        parts.append("</ul></details>")

    parts.extend(["</main>", "</body>", "</html>", ""])
    out_path = out_dir / f"{stem}.html"
    out_path.write_text("\n".join(parts), encoding="utf-8")
    return out_path


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: docx_to_sotm_html.py OUT_DIR DOCX...", file=sys.stderr)
        return 2
    out_dir = Path(argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    for path in map(Path, argv[2:]):
        out = convert_one(path, out_dir)
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
