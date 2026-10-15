#!/usr/bin/env python3
"""Render the manuscript to PDF with headless Chrome.

    .venv/bin/python scripts/build_pdf.py

Reads FINAL_PROJECT_22128981_GideonElormGlago.md, inlines every referenced figure
as a data URI, writes build/<stem>.html and <stem>.pdf at the repository root.
"""

from __future__ import annotations

import base64
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
STEM = "FINAL_PROJECT_22128981_GideonElormGlago"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }
body { font-family: "Georgia", "Times New Roman", serif; font-size: 10.6pt; line-height: 1.45; color: #111; }
h1 { font-size: 19pt; text-align: center; margin: 0 0 4pt; line-height: 1.2; }
h1 + p { text-align: center; font-size: 12pt; font-style: italic; margin-top: 0; }
.authors { text-align: center; margin: 10pt 0 16pt; line-height: 1.5; }
h2 { font-size: 13pt; margin: 18pt 0 6pt; border-bottom: 1px solid #ccc; padding-bottom: 2pt; break-after: avoid; }
h3 { font-size: 11.2pt; margin: 12pt 0 4pt; break-after: avoid; }
p { margin: 0 0 7pt; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 8.6pt; font-family: "Helvetica Neue", Arial, sans-serif; break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #eef1f5; }
blockquote { margin: 6pt 18pt; padding-left: 8pt; border-left: 3px solid #bbb; font-style: italic; color: #333; }
code { font-family: Menlo, Consolas, monospace; font-size: 8.8pt; background: #f4f4f4; padding: 0 2pt; }
pre { background: #f6f6f6; padding: 6pt; font-size: 8.5pt; overflow-x: hidden; white-space: pre-wrap; }
figure { margin: 8pt 0 12pt; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; }
figcaption { font-size: 8.8pt; color: #333; margin-top: 3pt; text-align: left; }
.refs p { text-align: left; padding-left: 18pt; text-indent: -18pt; font-size: 9.4pt; }
hr { border: 0; border-top: 1px solid #ddd; margin: 12pt 0; }
"""


def inline_figures(md: str) -> str:
    def repl(m: re.Match) -> str:
        caption, path = m.group(1), ROOT / m.group(2)
        data = base64.b64encode(path.read_bytes()).decode()
        return (f'<figure><img src="data:image/png;base64,{data}"/>'
                f"<figcaption>{caption}</figcaption></figure>")
    return re.sub(r"!\[(.+?)\]\((reports/figures/[^)]+)\)", repl, md)


def main() -> int:
    src = ROOT / f"{STEM}.md"
    body = markdown.markdown(inline_figures(src.read_text()), extensions=["tables", "fenced_code"])
    body = body.replace("<h2>References</h2>", '<h2>References</h2><div class="refs">') + "</div>"
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    page = build / f"{STEM}.html"
    page.write_text(html)
    pdf = ROOT / f"{STEM}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", page.as_uri()], check=True, capture_output=True)
    print(f"{pdf.name}  ({pdf.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
