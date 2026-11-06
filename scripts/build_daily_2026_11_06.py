#!/usr/bin/env python3
"""一次性生成 2026-11-06 五案卷 HTML（复用 build_account_pages 主题）。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_account_pages import (  # noqa: E402
    build_page,
    first_h1_plain,
    md_to_html_body,
)

# (输出 html 文件名 stem, markdown 文件名, 页内 tag)
BATCH = [
    ("2026-11-06-op7418", "2026-11-06-op7418.md", "可学 · 中文AI工具"),
    ("2026-11-06-vista8", "2026-11-06-vista8.md", "可学 · 华语PM"),
    ("2026-11-06-swyx", "2026-11-06-swyx.md", "可学 · AI eng"),
    ("2026-11-06-simonw", "2026-11-06-simonw.md", "可学 · indie开源"),
    ("2026-11-06-rowancheung", "2026-11-06-rowancheung.md", "可学 · AI newsletter"),
]


def main() -> None:
    out = ROOT / "docs" / "accounts"
    out.mkdir(parents=True, exist_ok=True)
    for slug, md_name, tag_label in BATCH:
        md_path = ROOT / "accounts" / md_name
        md_text = md_path.read_text(encoding="utf-8")
        html = build_page(
            title_text=first_h1_plain(md_text),
            body_html=md_to_html_body(md_text),
            tag_label=tag_label,
            back_href="../index.html",
            page_slug=slug,
        )
        out_path = out / f"{slug}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
