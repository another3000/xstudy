#!/usr/bin/env python3
"""从 accounts/specials/2610top40/profiles/*.md 生成专题 hub 与 40 份详情 HTML。"""

from __future__ import annotations

import re
from pathlib import Path

from build_account_pages import (
    AI_BADGE_HTML,
    SHELL_CSS,
    build_page,
    first_h1_plain,
    md_to_html_body,
)

ROOT = Path(__file__).resolve().parents[1]
SPECIAL_ROOT = ROOT / "accounts" / "specials" / "2610top40"
PROFILES_DIR = SPECIAL_ROOT / "profiles"
OUT_DIR = ROOT / "docs" / "specials" / "2610top40"
SOURCE_CREDIT = "https://x.com/jiao_newlife/status/2113932266267398206"
GITHUB_BASE = "https://github.com/another3000/xstudy/blob/main/accounts/specials/2610top40/profiles"

PROFILE_RE = re.compile(r"^(\d{2})-(.+)\.md$")


def load_index_meta() -> dict[int, dict[str, str]]:
    """从 profiles/INDEX.md 解析名次 → takeaway、判定（若有）。"""
    index_path = PROFILES_DIR / "INDEX.md"
    text = index_path.read_text(encoding="utf-8")
    meta: dict[int, dict[str, str]] = {}

    # Part1：| 1 | [名 @handle](file) | $amt | takeaway |
    for m in re.finditer(
        r"\|\s*(\d+)\s*\|\s*\[[^\]]+@([^\]]+)\]\(([^)]+)\)\s*\|\s*\$?([^|]+)\|\s*([^|]+)\|",
        text,
    ):
        rank = int(m.group(1))
        handle = m.group(2).strip()
        takeaway = m.group(5).strip()
        meta[rank] = {"handle": handle, "takeaway": takeaway, "verdict": ""}

    # Part2：| 21 | 逍遥子 | [@handle](file) | 458.80 | 判定 | 一句话 |
    for m in re.finditer(
        r"\|\s*(\d+)\s*\|\s*[^|]+\|\s*\[@([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|",
        text,
    ):
        rank = int(m.group(1))
        if rank < 21:
            continue
        handle = m.group(2).strip()
        amount = m.group(4).strip()
        verdict = m.group(5).strip()
        takeaway = m.group(6).strip()
        meta[rank] = {
            "handle": handle,
            "takeaway": takeaway,
            "verdict": verdict,
            "amount": amount,
        }

    return meta


def load_roster() -> list[dict[str, str]]:
    """解析 ROSTER.md 表格。"""
    roster_path = SPECIAL_ROOT / "ROSTER.md"
    rows: list[dict[str, str]] = []
    for line in roster_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("| 名次") or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 4 or not parts[0].isdigit():
            continue
        rows.append(
            {
                "rank": parts[0],
                "name": parts[1],
                "handle": parts[2],
                "amount": parts[3],
            }
        )
    return rows


def parse_verdict_from_profile(md_text: str) -> str:
    """从案卷首段「判定：」或 INDEX takeaway 的 🔴 推断绿/红边。"""
    for line in md_text.splitlines()[:8]:
        if "判定：" in line:
            return line.split("判定：", 1)[1].strip()
    return ""


def verdict_is_caution(verdict: str) -> bool:
    """红边慎学：判定里以慎学为主或半慎学。"""
    if not verdict:
        return False
    v = verdict.replace(" ", "")
    if "半可学" in v:
        return False
    if v.startswith("可学") and "慎学" not in v:
        return False
    if "慎学" in v:
        return True
    return False


def tag_label_for(rank: int, verdict: str) -> tuple[str, str]:
    """返回 (tag 文案, learn|caution)。"""
    if verdict_is_caution(verdict):
        return ("慎学 · 2610top40", "caution")
    return ("可学 · 2610top40", "learn")


def list_profiles() -> list[tuple[str, Path, int]]:
    """(slug, path, rank) 按名次排序。"""
    entries: list[tuple[str, Path, int]] = []
    for path in sorted(PROFILES_DIR.glob("*.md")):
        if path.name.startswith("_") or path.name in ("INDEX.md", "00-OVERVIEW.md"):
            continue
        m = PROFILE_RE.match(path.name)
        if not m:
            continue
        rank = int(m.group(1))
        slug = path.stem
        entries.append((slug, path, rank))
    entries.sort(key=lambda x: x[2])
    return entries


def build_detail_pages(index_meta: dict[int, dict[str, str]]) -> list[dict]:
    """生成 40 份详情页，返回 hub 行数据。"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    hub_rows: list[dict] = []

    for slug, path, rank in list_profiles():
        md_text = path.read_text(encoding="utf-8")
        title_text = first_h1_plain(md_text)
        body_html = md_to_html_body(md_text)
        meta = index_meta.get(rank, {})
        verdict = meta.get("verdict", "") or parse_verdict_from_profile(md_text)
        tag_label, kind = tag_label_for(rank, verdict)

        html = build_page(
            title_text=title_text,
            body_html=body_html,
            tag_label=tag_label,
            back_href="./index.html",
            page_slug=slug,
            assets_prefix="../../assets/",
        )
        (OUT_DIR / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"wrote specials/2610top40/{slug}.html")

        hub_rows.append(
            {
                "rank": rank,
                "slug": slug,
                "handle": meta.get("handle") or slug.split("-", 1)[-1],
                "takeaway": meta.get("takeaway", ""),
                "kind": kind,
                "tag_label": tag_label,
            }
        )

    return hub_rows


HUB_EXTRA_CSS = """
    .wrap { max-width: 920px; }
    .intro {
      background: var(--paper); border: 1px solid var(--line);
      padding: 20px 22px; margin: 12px 0 20px; border-left: 4px solid var(--gold);
      font-size: .92rem; color: var(--ink-soft);
    }
    .intro a { color: var(--pine); }
    .hub-table { width: 100%; border-collapse: collapse; font-size: .88rem; margin-top: 8px; }
    .hub-table th, .hub-table td {
      border: 1px solid var(--line); padding: 10px 12px; vertical-align: top; text-align: left;
    }
    .hub-table th { background: #ebe4d6; color: var(--ink-soft); letter-spacing: .06em; }
    .hub-table tr.learn { border-left: 3px solid var(--pine); }
    .hub-table tr.caution { border-left: 3px solid var(--cinnabar); }
    .hub-table .rank { font-weight: 700; color: var(--gold); white-space: nowrap; }
    .hub-table .amt { white-space: nowrap; font-variant-numeric: tabular-nums; }
    .pill {
      display: inline-block; font-size: .68rem; letter-spacing: .1em;
      padding: 2px 8px; border: 1px solid currentColor; margin-right: 6px;
    }
    .pill.learn { color: var(--pine); background: var(--pine-pale); }
    .pill.caution { color: var(--cinnabar); background: var(--cinnabar-pale); }
    .sub-tag {
      display: inline-block; margin-left: 8px; font-size: .72rem; color: var(--gold);
      letter-spacing: .14em;
    }
    .paper blockquote strong { color: var(--pine); }
"""


def build_hub(roster: list[dict[str, str]], hub_rows: list[dict]) -> None:
    """专题列表页。"""
    hub_rows.sort(key=lambda r: r["rank"])
    amount_by_rank = {int(r["rank"]): r["amount"] for r in roster}
    name_by_rank = {int(r["rank"]): r["name"] for r in roster}

    rows_html: list[str] = []
    for row in hub_rows:
        rank = row["rank"]
        amt = amount_by_rank.get(rank, "—")
        name = name_by_rank.get(rank, "")
        handle = row["handle"]
        kind = row["kind"]
        pill = "可学" if kind == "learn" else "慎学"
        takeaway = row["takeaway"] or "—"
        slug = row["slug"]
        rows_html.append(
            f"""<tr class="{kind}">
  <td class="rank">#{rank}</td>
  <td><span class="pill {kind}">{pill}</span><a href="{slug}.html">{name}</a><br/><span class="muted">@{handle}</span></td>
  <td class="amt">{amt}</td>
  <td>{takeaway}</td>
  <td><a href="{slug}.html">案卷</a></td>
</tr>"""
        )

    overview_md = (SPECIAL_ROOT / "OVERVIEW.md").read_text(encoding="utf-8")
    overview_html = md_to_html_body(overview_md)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>2610top40 晒单专题 · 山中学堂</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Ma+Shan+Zheng&display=swap" rel="stylesheet" />
  <style>
{SHELL_CSS}
{HUB_EXTRA_CSS}
    .muted {{ color: var(--muted); font-size: .82rem; }}
  </style>
</head>
<body>
<div class="wrap">
  <header class="site-hd">
    <a class="back" href="../../index.html">返回学堂</a>
    <span class="site-brand">山中学堂</span>
  </header>
  {AI_BADGE_HTML}
  <p class="sub-tag">晒单专题 · 商学院×实战派</p>
  <div class="paper learn">
    <h1>2610top40 专题</h1>
    <p>中文圈创作者公开晒单 TOP40｜学结构与叙事，不学押注标的。</p>
    <p class="muted">来源：<a href="{SOURCE_CREDIT}" rel="noopener">骄骄 @jiao_newlife 晒单帖</a></p>
  </div>
  <div class="intro">
    <strong>怎么读：</strong>绿边可学机制迁移；红边慎学互关、喊单、擦边话术。金额均为对方自报晒单，非审计财报。
  </div>
  <div class="paper learn">
    {overview_html}
  </div>
  <h2 style="margin:28px 0 12px; font-size:1.1rem; letter-spacing:.12em; color:var(--ink-soft);">全部 40 案卷</h2>
  <table class="hub-table">
    <thead>
      <tr><th>名次</th><th>账号</th><th>晒单 USD</th><th>一句话 takeaway</th><th></th></tr>
    </thead>
    <tbody>
{chr(10).join(rows_html)}
    </tbody>
  </table>
</div>
</body>
</html>
"""
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")
    print("wrote specials/2610top40/index.html")


def main() -> None:
    index_meta = load_index_meta()
    roster = load_roster()
    hub_rows = build_detail_pages(index_meta)
    build_hub(roster, hub_rows)


if __name__ == "__main__":
    main()
