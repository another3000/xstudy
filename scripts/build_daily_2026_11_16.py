#!/usr/bin/env python3
"""生成 2026-11-16 五案卷 HTML（指定头图轮换）。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_account_pages import (  # noqa: E402
    AI_BADGE_HTML,
    SHELL_CSS,
    first_h1_plain,
    md_to_html_body,
    paper_class,
    tag_class,
)

ASSETS = ROOT / "docs" / "assets"

BATCH = [
    (
        "2026-11-16-luoleiorg",
        "2026-11-16-luoleiorg.md",
        "可学 · 华语现场/社群",
        ("detail-b.jpg", "detail-c.jpg"),
    ),
    (
        "2026-11-16-lencx_",
        "2026-11-16-lencx_.md",
        "可学 · 华语工具深转译",
        ("detail-d.jpg", "detail-e.jpg"),
    ),
    (
        "2026-11-16-DIYgod",
        "2026-11-16-DIYgod.md",
        "可学 · 开源产品现场",
        ("detail-f.jpg", "detail-a.jpg"),
    ),
    (
        "2026-11-16-mattshumer_",
        "2026-11-16-mattshumer_.md",
        "可学 · 公开建造闭环",
        ("detail-c.jpg", "detail-a.jpg"),
    ),
    (
        "2026-11-16-AravSrinivas",
        "2026-11-16-AravSrinivas.md",
        "可学 · 出海GTM/产品数字",
        ("detail-e.jpg", "detail-a.jpg"),
    ),
]


def pick_banner(primary: str, fallback: str) -> str:
    if (ASSETS / primary).is_file():
        return primary
    return fallback


def build_page_with_banner(
    *,
    title_text: str,
    body_html: str,
    tag_label: str,
    banner_file: str,
) -> str:
    page_title = f"{title_text} · 山中学堂"
    pclass = paper_class(tag_label)
    tclass = tag_class(tag_label)
    banner_html = (
        f'<img class="detail-banner" src="../assets/{banner_file}" '
        f'alt="水墨山水案卷头图" width="820" height="200" loading="lazy" />'
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Ma+Shan+Zheng&display=swap" rel="stylesheet" />
  <style>
{SHELL_CSS}
  </style>
</head>
<body>
<div class="wrap">
  <header class="site-hd">
    <a class="back" href="../index.html">返回学堂</a>
    <span class="site-brand">山中学堂</span>
  </header>
  {AI_BADGE_HTML}
  {banner_html}
  <div class="{pclass}">
    <span class="{tclass}">{tag_label}</span>
    {body_html}
  </div>
</div>
</body>
</html>
"""


def main() -> None:
    out = ROOT / "docs" / "accounts"
    out.mkdir(parents=True, exist_ok=True)
    for slug, md_name, tag_label, (primary, fallback) in BATCH:
        md_path = ROOT / "accounts" / md_name
        md_text = md_path.read_text(encoding="utf-8")
        banner = pick_banner(primary, fallback)
        html = build_page_with_banner(
            title_text=first_h1_plain(md_text),
            body_html=md_to_html_body(md_text),
            tag_label=tag_label,
            banner_file=banner,
        )
        out_path = out / f"{slug}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"wrote {out_path.relative_to(ROOT)} ({banner})")


if __name__ == "__main__":
    main()