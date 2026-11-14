#!/usr/bin/env python3
"""生成 2026-11-14 五案卷 HTML（复用 build_account_pages 主题）。"""

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

BATCH = [
    ("2026-11-14-Linmiv", "2026-11-14-Linmiv.md", "可学 · 华语小产品/AI笔记"),
    ("2026-11-14-Livid", "2026-11-14-Livid.md", "可学 · 华语工具发车"),
    ("2026-11-14-xuanwo", "2026-11-14-xuanwo.md", "可学 · 华语 AI 工程工作流"),
    ("2026-11-14-HamelHusain", "2026-11-14-HamelHusain.md", "可学 · AI evals"),
    ("2026-11-14-sh_reya", "2026-11-14-sh_reya.md", "可学 · 数据/BI + evals"),
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
