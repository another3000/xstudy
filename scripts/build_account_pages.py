#!/usr/bin/env python3
"""从 accounts/*.md 生成 docs/accounts/{handle}.html（山中学堂主题）。"""

from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]

# handle -> (markdown 文件名不含路径, 页面副标题 tag 文案)
ACCOUNTS = [
    ("op7418", "2026-10-24-op7418.md", "可学 · 中文区"),
    ("dotey", "2026-10-24-dotey.md", "可学 · 中文区"),
    ("oran_ge", "2026-10-24-oran_ge.md", "可学 · 中文区"),
    ("vista8", "2026-10-24-vista8.md", "可学 · 中文区"),
    ("JessiCao_JC", "2026-10-24-jessicao_jc.md", "可学 · 中文区"),
    ("levelsio", "2026-10-24-levelsio.md", "可学 · 外文区"),
    ("swyx", "2026-10-24-swyx.md", "可学 · 外文区"),
    ("simonw", "2026-10-24-simonw.md", "可学 · 外文区"),
    ("lennysan", "2026-10-24-lennysan.md", "可学 · 外文区"),
    ("tibo_maker", "2026-10-24-tibo_maker.md", "可学 · 外文区"),
]

SHELL_CSS = """
    :root {
      --bg: #e8e2d4;
      --paper: rgba(252, 249, 240, 0.94);
      --ink: #1a1f1c;
      --ink-soft: #3a433c;
      --muted: #5c665e;
      --line: #c5b9a4;
      --pine: #2d5a45;
      --pine-pale: #dce8e1;
      --cinnabar: #9c2f24;
      --cinnabar-pale: #f3e4e1;
      --gold: #8a7340;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; min-height: 100vh;
      font-family: "Noto Serif SC", "Songti SC", "SimSun", serif;
      color: var(--ink); line-height: 1.75;
      background-color: var(--bg);
      background-image:
        radial-gradient(ellipse 90% 55% at 8% 0%, rgba(180, 200, 190, 0.55) 0%, transparent 58%),
        radial-gradient(ellipse 70% 45% at 92% 8%, rgba(200, 190, 160, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse 60% 40% at 50% 100%, rgba(140, 160, 150, 0.25) 0%, transparent 55%),
        linear-gradient(180deg, #ebe6d8 0%, #e4dfd0 40%, #d9e0d8 100%);
      background-attachment: fixed;
    }
    body::before {
      content: "";
      position: fixed; left: 0; right: 0; bottom: 0; height: 28vh;
      pointer-events: none; z-index: 0; opacity: 0.35;
      background:
        radial-gradient(ellipse 45% 80% at 12% 100%, #6a7d72 0%, transparent 70%),
        radial-gradient(ellipse 55% 90% at 48% 110%, #5a6e64 0%, transparent 68%),
        radial-gradient(ellipse 40% 70% at 82% 100%, #74887c 0%, transparent 70%);
    }
    .wrap { position: relative; z-index: 1; max-width: 820px; margin: 0 auto; padding: 32px 20px 72px; }
    .site-hd {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 6px; font-size: .88rem;
    }
    .back { color: var(--pine); text-decoration: none; letter-spacing: .1em; border-bottom: 1px solid #b7cfc2; }
    .back:hover { border-bottom-color: var(--pine); }
    .site-brand {
      font-family: "Ma Shan Zheng", "Noto Serif SC", serif;
      color: var(--gold); letter-spacing: .22em; font-size: 1.05rem;
    }
    .paper {
      background: var(--paper); color: var(--ink);
      padding: 28px 26px; margin-top: 10px;
      border: 1px solid var(--line); border-radius: 2px;
      box-shadow: 0 1px 0 rgba(26, 31, 28, 0.04);
      border-left: 4px solid var(--pine);
    }
    .paper h1 { margin: 8px 0 4px; font-size: 1.45rem; font-weight: 600; letter-spacing: .04em; }
    .paper h2 {
      margin: 1.55em 0 0.45em; font-size: 1.05rem; font-weight: 600;
      color: var(--ink-soft); border-bottom: 1px solid var(--line);
      padding-bottom: 0.35em; letter-spacing: 0.06em;
    }
    .paper h3 { margin: 1.2em 0 0.4em; font-size: 0.98rem; font-weight: 600; color: var(--ink-soft); }
    .tag {
      display: inline-block; font-size: 0.7rem; letter-spacing: 0.12em;
      padding: 2px 8px; margin: 0 6px 8px 0; border: 1px solid currentColor;
      color: var(--pine); background: var(--pine-pale);
    }
    .paper table { border-collapse: collapse; width: 100%; font-size: 0.9rem; margin: 10px 0 6px; }
    .paper th, .paper td { border: 1px solid var(--line); padding: 8px 10px; vertical-align: top; text-align: left; }
    .paper th { background: #ebe4d6; font-weight: 600; color: var(--ink-soft); }
    .paper a { color: var(--pine); }
    .paper a:hover { color: #234a38; }
    .paper ul, .paper ol { padding-left: 1.15em; }
    .paper li { margin: 0.35em 0; }
    .paper p { margin: 0.55em 0; }
    .paper strong { font-weight: 650; }
    .paper blockquote {
      margin: 0.6em 0; padding: 0.4em 12px;
      border-left: 3px solid var(--gold); color: var(--muted); font-size: 0.92rem;
      background: rgba(247, 243, 232, 0.5);
    }
    .paper code { font-size: 0.9em; background: rgba(232, 226, 212, 0.6); padding: 0 4px; }
    .paper em { color: var(--muted); }
"""


def md_to_html_body(text: str) -> str:
    """Markdown 转 HTML 片段。"""
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )


def first_h1_plain(md: str) -> str:
    """取首行 # 标题纯文本，用于 <title>。"""
    for line in md.splitlines():
        if line.startswith("# "):
            return re.sub(r"<[^>]+>", "", line[2:].strip())
    return "案卷"


def build_page(handle: str, md_name: str, tag_label: str) -> str:
    md_path = ROOT / "accounts" / md_name
    md_text = md_path.read_text(encoding="utf-8")
    title_text = first_h1_plain(md_text)
    body_html = md_to_html_body(md_text)
    page_title = f"{title_text} · 山中学堂"
    md_github = f"https://github.com/another3000/xstudy/blob/main/accounts/{md_name}"

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
  <div class="paper learn">
    <span class="tag learn">{tag_label}</span>
    {body_html}
  </div>
</div>
</body>
</html>
"""


def main() -> None:
    out_dir = ROOT / "docs" / "accounts"
    out_dir.mkdir(parents=True, exist_ok=True)
    for handle, md_name, tag_label in ACCOUNTS:
        html = build_page(handle, md_name, tag_label)
        (out_dir / f"{handle}.html").write_text(html, encoding="utf-8")
        print(f"wrote {handle}.html")


if __name__ == "__main__":
    main()
