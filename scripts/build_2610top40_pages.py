#!/usr/bin/env python3
"""从 accounts/specials/2610top40/profiles/*.md 生成专题 hub 与 40 份详情 HTML。"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
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

MECH_HEADER_RE = re.compile(r"^##\s+([^｜\n]+)｜(.+)$", re.MULTILINE)
MECH_MIGRATE_RE = re.compile(
    r"-\s*\*\*(LIS|输血|AI入企|小程序)：\*\*\s*(.+?)(?=\n- \*\*|\n\*\*本周实验|\Z)",
    re.DOTALL,
)
MECH_SOURCE_RE = re.compile(
    r"\*\*来源案卷：\*\*\s*\[#(\d+)\s+@([^\]]+)\]\(([^)]+)\)"
)


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


@dataclass
class MechanismCard:
    """机制卡：由 MECHANISMS.md 解析。"""

    card_id: str
    title: str
    verdict: str  # 可学 | 慎学
    hook: str
    explanation: str
    migrate: dict[str, str] = field(default_factory=dict)
    experiment: str = ""
    source_rank: int = 0
    source_handle: str = ""
    source_profile: str = ""


@dataclass
class WeeklyLearning:
    """本周学习：由 WEEKLY.md 解析。"""

    mechanism_id: str
    mechanism_title: str
    mechanism_blurb: str
    experiment_md: str
    priority_readers: list[dict[str, str]]


def _clean_field(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def load_mechanisms() -> list[MechanismCard]:
    """解析 accounts/specials/2610top40/MECHANISMS.md。"""
    path = SPECIAL_ROOT / "MECHANISMS.md"
    raw = path.read_text(encoding="utf-8")
    cards: list[MechanismCard] = []
    chunks = re.split(r"\n---\n", raw)
    for chunk in chunks:
        header = MECH_HEADER_RE.search(chunk)
        if not header:
            continue
        card_id = header.group(1).strip()
        title = header.group(2).strip()
        body = chunk[header.end() :]

        verdict_m = re.search(r"\*\*判定：\*\*\s*(\S+)", body)
        verdict = verdict_m.group(1).strip() if verdict_m else "可学"

        def field_val(name: str) -> str:
            m = re.search(
                rf"\*\*{name}：\*\*\s*(.+?)(?=\n\*\*|\n\*\*迁业务|\Z)",
                body,
                re.DOTALL,
            )
            return _clean_field(m.group(1)) if m else ""

        migrate: dict[str, str] = {}
        for m in MECH_MIGRATE_RE.finditer(body):
            migrate[m.group(1)] = _clean_field(m.group(2))

        src = MECH_SOURCE_RE.search(body)
        rank = int(src.group(1)) if src else 0
        handle = src.group(2).strip() if src else ""
        profile = src.group(3).strip() if src else ""

        cards.append(
            MechanismCard(
                card_id=card_id,
                title=title,
                verdict=verdict,
                hook=field_val("钩子公式"),
                explanation=field_val("机制说明"),
                migrate=migrate,
                experiment=field_val("本周实验"),
                source_rank=rank,
                source_handle=handle,
                source_profile=profile,
            )
        )
    return cards


def load_weekly(mechanisms: list[MechanismCard]) -> WeeklyLearning:
    """解析 accounts/specials/2610top40/WEEKLY.md。"""
    path = SPECIAL_ROOT / "WEEKLY.md"
    text = path.read_text(encoding="utf-8")

    mech_id_m = re.search(r"\*\*机制 id：\*\*\s*`([^`]+)`", text)
    mech_title_m = re.search(r"\*\*机制名：\*\*\s*(.+)", text)
    mech_blurb_m = re.search(r"\*\*一句话：\*\*\s*(.+)", text)
    mechanism_id = mech_id_m.group(1).strip() if mech_id_m else ""
    mechanism_title = mech_title_m.group(1).strip() if mech_title_m else ""
    mechanism_blurb = mech_blurb_m.group(1).strip() if mech_blurb_m else ""

    exp_block_m = re.search(
        r"## 本周实验[^\n]*\n\n(.+?)(?=\n## |\Z)",
        text,
        re.DOTALL,
    )
    experiment_md = exp_block_m.group(1).strip() if exp_block_m else ""

    priority: list[dict[str, str]] = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("| 名次 |"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 4 and parts[0].isdigit():
                priority.append(
                    {
                        "rank": parts[0],
                        "label": parts[1],
                        "keyword": parts[2],
                        "html": parts[3],
                    }
                )
        elif in_table and not line.startswith("|"):
            in_table = False

    if not mechanism_title and mechanism_id:
        for c in mechanisms:
            if c.card_id == mechanism_id:
                mechanism_title = c.title
                break

    return WeeklyLearning(
        mechanism_id=mechanism_id,
        mechanism_title=mechanism_title,
        mechanism_blurb=mechanism_blurb,
        experiment_md=experiment_md,
        priority_readers=priority,
    )


def render_learning_panel(
    weekly: WeeklyLearning, mechanisms: list[MechanismCard]
) -> str:
    """生成 hub 顶部学习面板 HTML。"""
    pick = next((c for c in mechanisms if c.card_id == weekly.mechanism_id), None)
    pick_hook = pick.hook if pick else ""
    pick_kind = "caution" if pick and pick.verdict == "慎学" else "learn"

    exp_html = md_to_html_body(weekly.experiment_md)
    exp_html = re.sub(r"^<p>|</p>$", "", exp_html.strip())

    priority_items = []
    for row in weekly.priority_readers:
        priority_items.append(
            f'<li><span class="pr-rank">#{html.escape(row["rank"])}</span> '
            f'<a href="{html.escape(row["html"])}">{html.escape(row["label"])}</a>'
            f' <span class="muted">· {html.escape(row["keyword"])}</span></li>'
        )

    cards_html: list[str] = []
    for card in mechanisms:
        kind = "caution" if card.verdict == "慎学" else "learn"
        pill = card.verdict
        migrate_bits = " · ".join(
            f"<strong>{k}</strong> {html.escape(v)}"
            for k, v in card.migrate.items()
        )
        profile_link = ""
        if card.source_rank and card.source_handle:
            slug = f"{card.source_rank:02d}-{card.source_handle}"
            if card.source_profile:
                slug_m = re.search(r"profiles/(\d{2}-[^)]+)\.md", card.source_profile)
                if slug_m:
                    slug = slug_m.group(1)
            profile_link = (
                f'<p class="card-src"><a href="{html.escape(slug)}.html">'
                f"#{card.source_rank} @{html.escape(card.source_handle)} 案卷</a></p>"
            )

        inner = f"""
      <p class="card-hook"><strong>钩子：</strong>{html.escape(card.hook)}</p>
      <p class="card-body">{html.escape(card.explanation)}</p>
      <p class="card-migrate">{migrate_bits}</p>
      <p class="card-exp"><strong>本周实验：</strong>{html.escape(card.experiment)}</p>
      {profile_link}
"""
        if kind == "caution":
            cards_html.append(
                f"""<details class="mech-card {kind}" id="{html.escape(card.card_id)}">
  <summary><span class="pill {kind}">{pill}</span> <span class="card-title">{html.escape(card.title)}</span>
    <span class="card-id muted">{html.escape(card.card_id)}</span></summary>
  <div class="card-inner">{inner}</div>
</details>"""
            )
        else:
            cards_html.append(
                f"""<article class="mech-card {kind}" id="{html.escape(card.card_id)}">
  <header><span class="pill {kind}">{pill}</span> <h3 class="card-title">{html.escape(card.title)}</h3>
    <span class="card-id muted">{html.escape(card.card_id)}</span></header>
  <div class="card-inner">{inner}</div>
</article>"""
            )

    return f"""
  <section class="learning-panel" aria-labelledby="learning-h">
    <h2 id="learning-h" style="margin:24px 0 12px; font-size:1.15rem; letter-spacing:.12em; color:var(--ink-soft);">学习层 · 机制卡</h2>
    <div class="weekly-hero paper {pick_kind}">
      <p class="weekly-label">本周必抄机制</p>
      <h3 class="weekly-title">{html.escape(weekly.mechanism_title)}</h3>
      <p class="muted card-id">id: <code>{html.escape(weekly.mechanism_id)}</code></p>
      <p>{html.escape(weekly.mechanism_blurb)}</p>
      {f'<p class="weekly-hook"><strong>钩子公式：</strong>{html.escape(pick_hook)}</p>' if pick_hook else ''}
      <div class="weekly-exp">
        <p class="weekly-label">本周实验</p>
        {exp_html}
      </div>
    </div>
    <div class="priority-eight">
      <p class="weekly-label">优先精读 8 人</p>
      <ul class="priority-list">
{chr(10).join(priority_items)}
      </ul>
    </div>
    <div class="mech-grid" role="list">
{chr(10).join(cards_html)}
    </div>
    <p class="muted" style="font-size:.82rem; margin-top:12px;">机制卡源文件：<code>accounts/specials/2610top40/MECHANISMS.md</code> · 本周：<code>WEEKLY.md</code></p>
  </section>
"""


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
    .learning-panel { margin: 8px 0 28px; }
    .weekly-hero { padding: 20px 22px; margin-bottom: 16px; }
    .weekly-hero.learn { border-left: 4px solid var(--pine); }
    .weekly-hero.caution { border-left: 4px solid var(--cinnabar); }
    .weekly-label {
      font-size: .72rem; letter-spacing: .18em; color: var(--gold); margin: 0 0 6px;
    }
    .weekly-title { margin: 0 0 8px; font-size: 1.12rem; }
    .weekly-hook { font-size: .92rem; color: var(--ink-soft); }
    .weekly-exp { margin-top: 14px; padding-top: 12px; border-top: 1px dashed var(--line); font-size: .9rem; }
    .priority-eight {
      background: var(--paper); border: 1px solid var(--line);
      padding: 14px 18px; margin-bottom: 18px;
    }
    .priority-list { list-style: none; padding: 0; margin: 8px 0 0; display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 6px 16px; font-size: .88rem; }
    .priority-list .pr-rank { color: var(--gold); font-weight: 700; margin-right: 6px; }
    .mech-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px;
    }
    .mech-card {
      background: var(--paper); border: 1px solid var(--line);
      padding: 14px 16px; font-size: .86rem; border-radius: 2px;
    }
    .mech-card.learn { border-left: 3px solid var(--pine); }
    .mech-card.caution {
      border-left: 3px solid var(--cinnabar); opacity: .92;
      background: rgba(252, 249, 240, 0.85);
    }
    .mech-card header { margin-bottom: 8px; }
    .mech-card .card-title { display: inline; font-size: .98rem; margin: 0; font-weight: 600; }
    .mech-card details summary {
      cursor: pointer; list-style: none; font-weight: 600;
    }
    .mech-card details summary::-webkit-details-marker { display: none; }
    .mech-card .card-inner { margin-top: 10px; }
    .mech-card .card-hook, .mech-card .card-body, .mech-card .card-migrate, .mech-card .card-exp {
      margin: 0.45em 0; color: var(--ink-soft);
    }
    .mech-card .card-migrate { font-size: .82rem; line-height: 1.55; }
    .mech-card .card-src { margin: 8px 0 0; font-size: .82rem; }
    .card-id { font-size: .75rem; }
"""


def build_hub(
    roster: list[dict[str, str]],
    hub_rows: list[dict],
    mechanisms: list[MechanismCard],
    weekly: WeeklyLearning,
) -> None:
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
    learning_html = render_learning_panel(weekly, mechanisms)

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
{learning_html}
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
    mechanisms = load_mechanisms()
    weekly = load_weekly(mechanisms)
    hub_rows = build_detail_pages(index_meta)
    build_hub(roster, hub_rows, mechanisms, weekly)


if __name__ == "__main__":
    main()
