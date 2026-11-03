#!/usr/bin/env python3
"""Validate published article JSON and build the static website output.

Every build writes real pages: home, archive, one page per article, about,
privacy, 404, sitemap.xml, robots.txt and feed.xml. Article JSON files in
content/articles/ stay the only content source, so daily publishing is
unchanged: add the JSON, run the tests and this build, push.

Output goes to dist/ (pushed to gh-pages) and is also synced to the
repository root, matching the existing convention that the root holds the
currently served site for local preview.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from xml.sax.saxutils import escape as xml_escape
import html
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "content" / "articles"
TOPICS_FILE = ROOT / "content" / "topic-queue.json"

# Final public address is MM's decision (architecture plan v1.0, decision 7).
# Until then, absolute URLs (canonical, social preview, sitemap, feed) use
# the documented GitHub Pages address. Tracked in ops/RELEASE_CHECKLIST.md.
SITE_URL = "https://plus-pro-max-ultra.github.io/remote-journal"
SITE_NAME = "遠方誌 | Journal for Far"
SITE_DESC = "遠方誌：從一個問題出發，讀懂歷史、科學、社會與日常背後的脈絡。"
TAIPEI = timezone(timedelta(hours=8))

ASSETS = ["stories.js", "manifest.webmanifest", "sw.js", "icon-192.png",
          "icon-512.png", "icon-180.png", "favicon-32.png", "favicon-16.png"]
REQUIRED = {"id", "title", "subtitle", "category", "tags", "minutes",
            "intro", "reflection", "sources", "date"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WEEKDAY_ZH = "一二三四五六日"


def esc(s):
    return html.escape(str(s), quote=True)


def cite_links(escaped_text):
    return re.sub(r"\[\^(\d+)\]", r'<sup class="cite"><a href="#src-\1">[\1]</a></sup>', escaped_text)


def source_parts(src):
    if isinstance(src, list):
        return {"title": src[0] if src else "", "url": src[1] if len(src) > 1 else "", "supports": ""}
    if isinstance(src, dict):
        return {"title": src.get("title", ""), "url": src.get("url", ""), "supports": src.get("supports", "")}
    return {"title": "", "url": "", "supports": ""}


def safe_url(raw):
    return raw if isinstance(raw, str) and raw.startswith("https://") else ""


def story_figures(story, pos, prefix):
    out = []
    for im in story.get("images", []):
        if im.get("after") != pos:
            continue
        cls = "story-fig"
        if im.get("size") == "medium":
            cls += " fig-medium"
        elif im.get("size") == "small":
            cls += " fig-small"
        src = im.get("src", "")
        if src.startswith("assets/"):
            src = prefix + src
        credit = esc(im.get("credit", ""))
        if im.get("source"):
            credit = f'<a href="{esc(im["source"])}" target="_blank" rel="noopener noreferrer">{credit}</a>'
        out.append(f'<figure class="{cls}"><img src="{esc(src)}" alt="{esc(im.get("alt", ""))}" loading="lazy">'
                   f'<figcaption>{esc(im.get("caption", ""))}<span class="fig-credit">{credit}</span></figcaption></figure>')
    return "".join(out)


def render_body(story, prefix):
    if isinstance(story.get("sections"), list):
        parts = []
        for i, sec in enumerate(story["sections"], 1):
            block = "<h2>" + esc(sec.get("heading", "")) + "</h2>"
            block += "".join("<p>" + cite_links(esc(p)) + "</p>" for p in sec.get("paragraphs", []))
            if sec.get("quote"):
                block += "<blockquote>" + esc(sec["quote"]) + "</blockquote>"
            if sec.get("callout"):
                block += '<div class="callout">' + esc(sec["callout"]) + "</div>"
            if isinstance(sec.get("diagram"), list) and sec["diagram"]:
                items = "".join(f'<div class="flow-item">{esc(x)}</div>' for x in sec["diagram"])
                block += (f'<div class="diagram"><strong>本節的因果脈絡</strong>'
                          f'<div class="flow" style="margin-top:14px">{items}</div></div>')
            block += story_figures(story, "section-" + str(i), prefix)
            parts.append(block)
        return "".join(parts)
    # Early articles store trusted HTML in body (see PROJECT_STATUS 已知限制).
    return story.get("body", "")


def sources_html(story):
    srcs = [source_parts(x) for x in story.get("sources", [])]
    srcs = [x for x in srcs if safe_url(x["url"])]
    ev = [x for x in srcs if str(x["supports"]).strip()]
    fw = [x for x in srcs if not str(x["supports"]).strip()]
    ev_items = "".join(
        f'<li id="src-{i}"><a href="{esc(x["url"])}" target="_blank" rel="noopener noreferrer">'
        f'{esc(x["title"] or x["url"])} ↗</a>'
        f'<div class="meta" style="margin-top:4px">支持內容：{esc(x["supports"])}</div></li>'
        for i, x in enumerate(ev, 1))
    fw_items = "".join(
        f'<li><a href="{esc(x["url"])}" target="_blank" rel="noopener noreferrer">'
        f'{esc(x["title"] or x["url"])} ↗</a></li>'
        for x in fw)
    ev_block = ""
    if ev:
        ev_block = (f'<details class="srcblk"><summary><span>查證資料來源</span>'
                    f'<span class="src-count">{len(ev)} 項</span></summary>'
                    f'<p class="src-note">實際支持文中事實主張的來源，逐條標註支持的內容；文內如有 [數字] 標記，對應此處編號。</p>'
                    f"<ol>{ev_items}</ol></details>")
    fw_inner = ""
    if fw:
        fw_inner = (f'<p class="src-note">供進一步閱讀的資源；未逐條對應文中事實，內容以各來源頁為準。</p>'
                    f"<ol>{fw_items}</ol>")
    fw_count = f"{len(fw)} 項資源" if fw else ""
    fw_block = (f'<details class="srcblk"><summary><span>延伸探討</span><span class="src-count">{fw_count}</span></summary>'
                f"{fw_inner}"
                f'<div class="reflection"><div class="eyebrow">TAKE IT FURTHER</div><h3>把故事帶回自己的思考</h3>'
                f"<p>{esc(story.get('reflection', ''))}</p>"
                f'<textarea id="reflectionNote" placeholder="寫下你的想法、疑問，或之後想追查的線索……"></textarea>'
                f'<div class="save-note">筆記會儲存在目前瀏覽器，不會上傳或同步到其他裝置。</div></div></details>')
    return ev_block + fw_block or '<p class="src-note">此篇尚未補齊可核實的來源。</p>'


def head(title, desc, prefix, path, og_type="website", extra=""):
    url = SITE_URL + path
    lines = [
        "<!doctype html>",
        '<html lang="zh-Hant">',
        "<head>",
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
        '<meta name="theme-color" content="#f4f0e8">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(desc)}">',
        f'<link rel="canonical" href="{esc(url)}">',
        f'<meta property="og:site_name" content="{esc(SITE_NAME)}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:url" content="{esc(url)}">',
        f'<meta property="og:image" content="{SITE_URL}/icon-512.png">',
        f'<link rel="manifest" href="{prefix}manifest.webmanifest">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32.png">',
        f'<link rel="icon" type="image/png" sizes="16x16" href="{prefix}favicon-16.png">',
        f'<link rel="apple-touch-icon" href="{prefix}icon-180.png">',
        f'<link rel="stylesheet" href="{prefix}assets/site.css">',
        f'<link rel="alternate" type="application/rss+xml" title="{esc(SITE_NAME)} RSS" href="{SITE_URL}/feed.xml">',
        "<script>document.documentElement.classList.add('js')</script>",
    ]
    if extra:
        lines.append(extra)
    lines.append("</head>")
    return "\n".join(lines)


def topbar(prefix, saved_nav=False):
    saved = ' <button class="ghost js-only" id="savedNav">我的收藏 <span id="savedCount">0</span></button>' if saved_nav else ""
    return "\n".join([
        '<header class="topbar">',
        f'  <a class="brand" href="{prefix}" aria-label="回到遠方誌首頁"><img class="brandmark" src="{prefix}icon-192.png" alt="" width="34" height="34"><span><span class="brandname">遠方誌</span><span class="brandeng"><span class="brandsep" aria-hidden="true"> | </span>Journal for Far</span><br><span class="brandtag">把世界讀深一點</span></span></a>',
        f'  <nav class="top-actions"><a class="ghost" href="{prefix}archive/"><span class="wide-only">文章</span>索引</a> <a class="ghost wide-only" href="{prefix}about/">關於</a>{saved} <a class="solid" href="{prefix}archive/" data-surprise>帶我去遠方 ↗</a></nav>',
        "</header>",
    ])


def footer(prefix):
    return "\n".join([
        "<footer>",
        "  <div>遠方誌 · 一份讓好奇心有地方安放的閱讀刊物</div>",
        f'  <nav class="foot-nav" aria-label="網站導覽"><a href="{prefix}">首頁</a><a href="{prefix}archive/">文章索引</a><a href="{prefix}about/">關於本刊</a><a href="{prefix}privacy/">隱私權說明</a><a href="{prefix}feed.xml">RSS 訂閱</a></nav>',
        '  <div class="footnote-line">收藏與筆記只保存在目前瀏覽器，不會上傳或同步到其他裝置。</div>',
        '  <div class="footnote-line">© 2026 遠方誌 <span class="placeholder">版權聲明文字與授權方式待 MM 確認後定案</span></div>',
        "</footer>",
    ])


REVIEW_BANNER = '<div class="review-banner">本頁為草稿：內容與措辭待 MM 核准後才會正式生效。</div>'
TOAST_DIV = '<div class="toast" id="toast" role="status" aria-live="polite"></div>'


def scripts_tag(prefix):
    return f'<script src="{prefix}assets/site.js"></script>'


def search_text(story):
    return " ".join([story["title"], story["subtitle"], story["category"],
                     *story.get("tags", []), story.get("intro", "")]).lower()


def story_card(story, prefix, extra=False):
    cls = "article-card extra" if extra else "article-card"
    href = f"{prefix}articles/{story['id']}/"
    first_tag = (story.get("tags") or [story["category"]])[0]
    return (f'<article class="{cls}" data-id="{esc(story["id"])}" data-cat="{esc(story["category"])}" '
            f'data-search="{esc(search_text(story))}">'
            f'<div class="meta">{esc(story["num"])} / {esc(story["category"])} · {story["minutes"]} 分鐘</div>'
            f'<h3><a class="card-link" href="{href}">{esc(story["title"])}</a></h3>'
            f"<p>{esc(story['subtitle'])}</p>"
            f'<div class="card-bottom"><a class="text-btn" href="{href}">開始閱讀 ↗</a>'
            f'<span class="tag">{esc(first_tag)}</span></div></article>')


def add_days(dstr, n):
    return (datetime.strptime(dstr, "%Y-%m-%d") + timedelta(days=n)).strftime("%Y-%m-%d")


def weekday_zh(dstr):
    return WEEKDAY_ZH[datetime.strptime(dstr, "%Y-%m-%d").weekday()]


def topic_rows(stories, topics, today):
    taken = {s["date"] for s in stories}
    published = {s["id"] for s in stories}
    queue = [t for t in topics if t["id"] not in published]
    dates = []
    i = 1 if today in taken else 0
    while len(dates) < 7 and i < 40:
        dates.append(add_days(today, i))
        i += 1
    by_date = {t["date"]: t for t in queue if t["date"] >= today}
    rows = [{"date": t["date"], "topic": t, "delayed": True}
            for t in sorted((t for t in queue if t["date"] < today), key=lambda t: t["date"])]
    rows += [{"date": t["date"], "topic": t, "delayed": True}
             for t in queue if t["date"] >= today and t["date"] in taken and t["date"] in dates]
    rows += [{"date": d, "topic": by_date.get(d), "delayed": False} for d in dates]
    return rows


def topic_rows_html(rows):
    out = []
    for r in rows:
        label = ("原定 " if r["delayed"] else "") + r["date"] + "（" + weekday_zh(r["date"]) + "）"
        meta = (f'<span class="topic-meta-line"><span class="topic-num">候選</span>'
                f'<span class="topic-date">{esc(label)}</span>')
        t = r["topic"]
        if not t:
            body = (meta + '<span class="topic-cat">研擬中</span></span>'
                    '<span class="topic-title" style="color:var(--muted)">題目確認後公布 '
                    '<span class="topic-badge">預告</span></span>')
        else:
            badge = "順延・研究中" if r["delayed"] else "預告・研究中"
            body = (meta + f'<span class="topic-cat">{esc(t["category"])}</span></span>'
                    f'<span class="topic-title">{esc(t["title"])} '
                    f'<span class="topic-badge">{badge}</span></span>')
        out.append('<div class="topic-row preview">' + body + '</div>')
    return "".join(out)


def build_home(stories, topics):
    prefix = "./"
    latest = stories[-1]
    side = stories[max(0, len(stories) - 3):len(stories) - 1]
    cards = list(reversed(stories))
    grid = "".join(story_card(s, prefix, extra=(i >= 6)) for i, s in enumerate(cards))
    issue_range = stories[0]["num"] + "—" + stories[-1]["num"]
    feature = (
        f'<article class="feature"><div class="feature-num" aria-hidden="true">{esc(latest["num"])}</div>'
        f'<div><div class="eyebrow">TODAY\'S SELECTION / {esc(latest["num"])}</div>'
        f'<div class="feature-date">{esc(latest["date"])} 刊出</div>'
        f'<h3><a class="card-link" href="./articles/{latest["id"]}/">{esc(latest["title"])}</a></h3>'
        f'<p>{esc(latest["subtitle"])}</p></div>'
        f'<div><span class="tag">{esc(latest["category"])}</span><br>'
        f'<a class="read-link text-btn" style="color:#fff" href="./articles/{latest["id"]}/">走進這個問題 ↗</a></div></article>')
    side_html = "".join(
        f'<article class="mini-feature"><div><div class="meta">{esc(s["num"])} / {esc(s["category"])}</div>'
        f'<h3><a class="card-link" href="./articles/{s["id"]}/">{esc(s["title"])}</a></h3>'
        f'<p>{s["minutes"]} 分鐘 · {"、".join(esc(t) for t in s.get("tags", [])[:2])}</p></div>'
        f'<a class="text-btn" href="./articles/{s["id"]}/" style="text-align:left;margin-top:14px">開始閱讀 ↗</a></article>'
        for s in side)
    today = datetime.now(TAIPEI).strftime("%Y-%m-%d")
    topics_html = topic_rows_html(topic_rows(stories, topics, today))
    extra_head = ('<script src="./stories.js"></script>\n'
                  + "<script>window.FARAWAY_TOPICS = " + json.dumps(topics, ensure_ascii=False) + ";</script>")
    parts = [
        head("遠方誌 | Journal for Far", SITE_DESC, prefix, "/", extra=extra_head),
        '<body data-root="./" data-page="home">',
        topbar(prefix, saved_nav=True),
        '<div class="shell home" id="homeView">',
        f'  <div class="edition-status" role="status"><span>最新刊期 {esc(latest["num"])} · {esc(latest["date"])}</span><span>每日出刊 · 台北時間</span></div>',
        '  <section class="hero">',
        '    <div><div class="eyebrow">A FIELD GUIDE TO THE WIDER WORLD</div><h1><span class="sl1">世界不只發生。</span><span class="sl2">它值得被理解。</span></h1><p>從一條塞車的道路、一個古老的制度，或一個反直覺的數字出發。沿著故事走進它的來處、機制與爭議，讀到新聞之外，也讀到世界如何運作。</p></div>',
        f'    <div class="hero-art" aria-label="抽象的道路與地平線插畫"><div class="art-line"></div><div class="art-circle"></div><div class="art-copy"><span>ISSUE NO. {issue_range}</span><strong>每個問題，<br>都是通往遠方的路。</strong></div></div>',
        "  </section>",
        "  <section>",
        '    <div class="section-head"><div><div class="eyebrow">A DAILY WINDOW ON THE WORLD</div><h2>今天，從一個問題開始</h2></div><div class="search js-only"><input id="searchInput" type="search" placeholder="搜尋主題、概念或領域…" aria-label="搜尋文章"><button class="ghost" id="clearSearch">清除</button></div></div>',
        '    <div class="filters" id="filters" aria-label="依領域篩選文章"></div>',
        f'    <div class="feature-grid" id="featureGrid">{feature}<div class="feature-side">{side_html}</div></div>',
        '    <div class="section-head"><div><div class="eyebrow">LATEST</div><h2 id="archiveTitle">最新文章</h2></div></div>',
        f'    <div class="article-grid" id="articleGrid">{grid}</div>',
        '    <div class="empty" id="emptyResult" style="display:none">沒有找到相符的文章。試試不同關鍵字，或清除篩選條件。</div>',
        f'    <div class="more-wrap" id="viewAllWrap"><a class="ghost" href="./archive/">查看全部文章（共 {len(stories)} 篇）→</a></div>',
        "  </section>",
        '  <section class="topics" id="topicIndex" aria-label="未來一週預告">',
        '    <div class="section-head"><div><div class="eyebrow">COMING WEEK</div><h2>未來一週預告</h2><p>下一週的候選選題；全部已刊出文章請見「文章索引」。</p></div></div>',
        f'    <div class="topic-block"><div class="topic-table" id="previewTopics">{topics_html}</div><p class="topic-note">預告為候選題目，日期為預定出刊日，可能依研究與查證調整；延期時保留「原定」日期標示。</p></div>',
        "  </section>",
        footer(prefix),
        "</div>",
        TOAST_DIV,
        scripts_tag(prefix),
        "</body></html>",
    ]
    return "\n".join(parts)


def build_archive(stories):
    prefix = "../"
    months = sorted({s["date"][:7] for s in stories}, reverse=True)
    options = '<option value="all">全部月份</option>' + "".join(
        f'<option value="{m}">{m.split("-")[0]} 年 {int(m.split("-")[1])} 月</option>' for m in months)
    rows = []
    last_month = None
    for s in sorted(stories, key=lambda x: (x["date"], x["num"]), reverse=True):
        m = s["date"][:7]
        if m != last_month:
            last_month = m
            rows.append(f'<div class="month-head" data-mh="{m}">{m.split("-")[0]} 年 {int(m.split("-")[1])} 月</div>')
        rows.append(
            f'<a class="topic-row" href="../articles/{s["id"]}/" data-id="{esc(s["id"])}" '
            f'data-cat="{esc(s["category"])}" data-month="{m}" data-search="{esc(search_text(s))}">'
            f'<span class="topic-meta-line"><span class="topic-num">{esc(s["num"])}</span>'
            f'<span class="topic-date">{esc(s["date"])}</span>'
            f'<span class="topic-cat">{esc(s["category"])}</span></span>'
            f'<span class="topic-title">{esc(s["title"])}</span></a>')
    parts = [
        head("文章索引 · 遠方誌", "遠方誌全部已刊出文章，依月份排列，可搜尋、依領域篩選。", prefix, "/archive/"),
        '<body data-root="../" data-page="archive">',
        topbar(prefix),
        '<div class="shell archive-page">',
        '  <div class="page-head"><div class="eyebrow">ARCHIVE</div><h2>文章索引</h2><p>依月份排列，可搜尋、依領域篩選；點任一題目直接閱讀。</p></div>',
        '  <div class="archive-tools js-only"><div class="search"><input id="archiveSearchInput" type="search" placeholder="搜尋主題、概念或領域…" aria-label="搜尋文章"><button class="ghost" id="archiveClear">清除</button></div>'
        f'<select class="mselect" id="archiveMonthSelect" aria-label="依月份篩選">{options}</select>'
        '<div class="filters" id="archiveFilters" aria-label="依領域篩選文章"></div></div>',
        f'  <div class="arch-count" id="archiveCount">共 {len(stories)} 篇</div>',
        f'  <div id="archiveList">{"".join(rows)}</div>',
        '  <div class="empty" id="archiveEmpty" style="display:none">沒有找到相符的文章。</div>',
        "</div>",
        footer(prefix),
        TOAST_DIV,
        scripts_tag(prefix),
        "</body></html>",
    ]
    return "\n".join(parts)


def build_article(stories, idx):
    s = stories[idx]
    nxt = stories[(idx + 1) % len(stories)]
    prefix = "../../"
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in s.get("tags", []))
    parts = [
        head(s["title"] + " · 遠方誌", s["subtitle"], prefix, "/articles/" + s["id"] + "/", og_type="article"),
        f'<body data-root="../../" data-page="article" data-id="{esc(s["id"])}">',
        topbar(prefix),
        '<main class="reader visible" id="readerView">',
        '  <a class="back" href="../../archive/">← 回到文章索引</a>',
        '  <article id="readerArticle">',
        f'    <header class="reader-head"><div class="eyebrow">FIELD NOTES / {esc(s["num"])}</div>'
        f'<div class="meta" style="margin-top:12px">{esc(s["category"])}　·　{esc(s["date"])} 刊出　·　{s["minutes"]} 分鐘閱讀</div>'
        f"<h1>{esc(s['title'])}</h1>"
        f'<p class="dek">{esc(s["subtitle"])}</p>'
        f'<div class="reader-meta">{tags}<span class="meta">一篇從現象走向機制的探索</span></div>'
        f'<div class="reader-actions"><button class="ghost bookmark js-only" id="bookmarkBtn">＋ 收藏這篇</button>'
        f'<button class="ghost js-only" id="printBtn">列印 / 存成 PDF</button>'
        f'<button class="ghost js-only" id="copyLinkBtn">複製文章連結</button></div></header>',
        f'    <div class="reader-body"><p>{cite_links(esc(s.get("intro", "")))}</p>'
        + story_figures(s, "intro", prefix) + render_body(s, prefix) + "</div>",
        f'    <section class="sources">{sources_html(s)}</section>',
        f'    <section class="next-read"><div><div class="meta">接著探索</div><h4>沿著另一條線索繼續走</h4></div>'
        f'<a class="solid" href="../{nxt["id"]}/">下一個故事 ↗</a></section>',
        "  </article>",
        "</main>",
        footer(prefix),
        TOAST_DIV,
        scripts_tag(prefix),
        "</body></html>",
    ]
    return "\n".join(parts)


# Draft pages for MM's review (architecture plan v1.0, items 4, 5 and 7).
# Marked with the review banner; contact route and final wording await MM.
ABOUT_BODY = """
<section class="prose">
<h2>這是一份什麼刊物</h2>
<p>遠方誌是一份閱讀型知識刊物：以具體的故事或問題為入口，交代脈絡、機制、證據與反例，帶讀者理解世界背後的運作方式。自 2026 年 10 月 25 日起，每個台北日期刊出一篇。</p>
<h2>文章如何產生</h2>
<p>每篇文章由編輯流程撰寫與查證：從一個可感知的現象或疑問出發，交代必要的背景，逐步拆解背後的機制，再檢驗證據、提出反例與適用邊界，最後把核心概念連結到另一個領域，並說清楚類比的限制。來源優先採用原始資料、官方統計、學術研究、博物館與檔案館、大學教材與專業機構文件；數字必須有來源、單位、年份與比較基準。每篇刊出前都逐條核對，查證不足就延後出刊，不為維持連載降低標準。</p>
<h2>來源如何標示</h2>
<p>每篇文章末尾列出「查證資料來源」與「延伸探討」：前者逐條標註實際支持的內容，文內如有 [數字] 標記即對應此處編號；後者供進一步閱讀，內容以各來源頁為準。文中提及數據的提供單位時，也會把連結嵌入相關文字，讀到就能點開查證。</p>
<h2>編輯獨立與內容聲明</h2>
<p>遠方誌內容不接受贊助，選題與寫作不由任何商業或政治機構決定。文章為一般性閱讀與知識探索，不構成醫療、法律、投資或其他專業建議；涉及專業領域的決定，請諮詢合格的專業人士。文中的詮釋與觀點屬於本刊，事實主張均附可查證的來源。</p>
<h2>聯絡方式</h2>
<p><span class="placeholder">聯絡管道待 MM 確認後補上。</span></p>
</section>
"""

PRIVACY_BODY = """
<section class="prose">
<h2>本刊收集什麼資料</h2>
<p>沒有。遠方誌沒有帳號、沒有表單、不安裝分析工具，也不放置廣告追蹤；閱讀不需要提供任何個人資料。</p>
<h2>瀏覽器本機儲存</h2>
<p>收藏與筆記只儲存在你所用瀏覽器的本機儲存空間，不會傳送到本刊或任何第三方；清除瀏覽器資料即可刪除。網站並使用 service worker 把頁面暫存在你的裝置上，供離線閱讀，這些內容同樣只存在你的裝置。</p>
<h2>託管服務必然處理的資料</h2>
<p>本站由第三方託管（目前為 GitHub Pages；新網址使用 Cloudflare Workers）。如同多數網站託管服務，託管方會依自己的隱私權政策處理標準連線紀錄，例如 IP 位址與存取時間：</p>
<ul>
<li><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub General Privacy Statement</a></li>
<li><a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener noreferrer">Cloudflare Privacy Policy</a></li>
</ul>
<h2>未來如有變動</h2>
<p>若未來啟用分析或廣告（每一項都需要另行決定），本頁會在功能上線前更新；屆時廣告會另外加上 Google 要求的 Cookie 與同意聲明。</p>
<h2>聯絡方式</h2>
<p>對本頁內容有疑問，請透過<span class="placeholder">聯絡管道待 MM 確認後補上</span>與我們聯繫。</p>
<p class="footnote-line">本頁最後更新：2026-11-04</p>
</section>
"""


def build_static_page(title, desc, path, eyebrow, heading, lede, body_html):
    prefix = "../"
    parts = [
        head(title, desc, prefix, path),
        '<body data-root="../" data-page="static">',
        topbar(prefix),
        '<div class="shell archive-page">',
        f'  <div class="page-head"><div class="eyebrow">{eyebrow}</div><h2>{heading}</h2><p>{lede}</p>{REVIEW_BANNER}</div>',
        body_html.strip(),
        "</div>",
        footer(prefix),
        TOAST_DIV,
        scripts_tag(prefix),
        "</body></html>",
    ]
    return "\n".join(parts)


def build_404():
    prefix = SITE_URL + "/"
    parts = [
        head("找不到這個頁面 · 遠方誌", "您要找的頁面不存在或已移動。", prefix, "/404.html"),
        f'<body data-root="{prefix}" data-page="404">',
        topbar(prefix),
        '<div class="shell archive-page">',
        '  <div class="page-head"><div class="eyebrow">404</div><h2>找不到這個頁面</h2><p>您要找的頁面不存在或已移動。舊的 # 連結會自動轉到對應的新頁面。</p></div>',
        f'  <section class="prose"><p><a href="{prefix}">回到首頁</a>，或到<a href="{prefix}archive/">文章索引</a>瀏覽全部文章。</p></section>',
        "</div>",
        footer(prefix),
        TOAST_DIV,
        scripts_tag(prefix),
        "</body></html>",
    ]
    return "\n".join(parts)


def build_feed(stories):
    items = []
    for s in reversed(stories):
        dt = datetime.strptime(s["date"], "%Y-%m-%d").replace(tzinfo=TAIPEI)
        link = f"{SITE_URL}/articles/{s['id']}/"
        items.append(f"<item><title>{xml_escape(s['title'])}</title><link>{link}</link>"
                     f'<guid isPermaLink="true">{link}</guid><pubDate>{format_datetime(dt)}</pubDate>'
                     f"<category>{xml_escape(s['category'])}</category>"
                     f"<description>{xml_escape(s['subtitle'])}</description></item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            f"<title>{xml_escape(SITE_NAME)}</title><link>{SITE_URL}/</link>"
            f"<description>{xml_escape(SITE_DESC)}</description><language>zh-Hant</language>"
            f"<lastBuildDate>{format_datetime(datetime.now(TAIPEI))}</lastBuildDate>"
            + "".join(items) + "</channel></rss>\n")


def build_sitemap(stories, build_date):
    urls = [("/", build_date), ("/archive/", build_date), ("/about/", build_date), ("/privacy/", build_date)]
    urls += [(f"/articles/{s['id']}/", s["date"]) for s in stories]
    body = "".join(f"<url><loc>{SITE_URL}{p}</loc><lastmod>{d}</lastmod></url>" for p, d in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + "</urlset>\n")


def build_robots():
    return "User-agent: *\nAllow: /\nSitemap: " + SITE_URL + "/sitemap.xml\n"


def source_url(src):
    return src[1] if isinstance(src, list) and len(src) > 1 else (src.get("url", "") if isinstance(src, dict) else "")


def main():
    paths = sorted(ARTICLES.glob("*.json"))
    stories = []
    ids = set()
    errors = []
    for path in paths:
        try:
            story = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{path.name}: JSON 讀取失敗：{e}")
            continue
        missing = REQUIRED - set(story)
        if missing:
            errors.append(f"{path.name}: 缺少欄位 {', '.join(sorted(missing))}")
        date = story.get("date", "")
        if not DATE_RE.match(str(date)):
            errors.append(f"{path.name}: date 必須是 YYYY-MM-DD 出刊日期：{date}")
        if not story.get("body") and not isinstance(story.get("sections"), list):
            errors.append(f"{path.name}: 必須有 body 或 sections")
        if not story.get("id") or story["id"] in ids:
            errors.append(f"{path.name}: id 空白或重複：{story.get('id')}")
        ids.add(story.get("id"))
        if not isinstance(story.get("tags"), list):
            errors.append(f"{path.name}: tags 必須是陣列")
        if not isinstance(story.get("sources"), list) or len(story.get("sources", [])) < 2:
            errors.append(f"{path.name}: 至少列出 2 個來源")
        for src in story.get("sources", []):
            url = source_url(src)
            if not isinstance(url, str) or not url.startswith("https://"):
                errors.append(f"{path.name}: 來源連結必須使用 HTTPS：{url}")
        img_after = re.compile(r"^(intro|section-[1-9][0-9]*)$")
        for im in story.get("images", []):
            src = im.get("src", "")
            if not src.startswith("assets/img/") or not (ROOT / src).is_file():
                errors.append(f"{path.name}: 圖片檔案不存在或路徑錯誤：{src}")
            for k in ("alt", "caption", "credit", "source"):
                if not im.get(k):
                    errors.append(f"{path.name}: 圖片缺少欄位 {k}：{src}")
            if not str(im.get("source", "")).startswith("https://"):
                errors.append(f"{path.name}: 圖片缺少 https 來源連結：{src}")
            if not img_after.match(str(im.get("after", ""))):
                errors.append(f"{path.name}: 圖片 after 位置無效：{im.get('after')}")
            if im.get("size", "wide") not in ("wide", "medium", "small"):
                errors.append(f"{path.name}: 圖片 size 無效：{im.get('size')}（限 wide/medium/small）")
        stories.append(story)
    if not TOPICS_FILE.is_file():
        errors.append("content/topic-queue.json 不存在")
        topics = []
    else:
        try:
            topics = json.loads(TOPICS_FILE.read_text(encoding="utf-8"))["queue"]
        except Exception as e:
            errors.append(f"topic-queue.json 讀取失敗：{e}")
            topics = []
    if errors:
        print("內容檢查失敗：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1

    for i, story in enumerate(stories, 1):
        story["num"] = f"{i:03d}"
        # Reading time from actual content length (~350 zh chars/min), so labels
        # never drift from the real article; the JSON "minutes" field is a fallback only.
        if isinstance(story.get("sections"), list):
            text = story.get("intro", "") + "".join(
                para for sec in story["sections"] for para in sec.get("paragraphs", []))
        else:
            text = story.get("intro", "") + re.sub(r"<[^>]+>", "", story.get("body", ""))
        story["minutes"] = max(1, round(len(re.sub(r"\s", "", text)) / 350))

    (ROOT / "stories.js").write_text(
        "// Generated by scripts/build_site.py. Edit content/articles/*.json instead.\n"
        "window.FARAWAY_STORIES = " + json.dumps(stories, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8")

    build_date = datetime.now(TAIPEI).strftime("%Y-%m-%d")
    pages = {
        "index.html": build_home(stories, topics),
        "archive/index.html": build_archive(stories),
        "about/index.html": build_static_page(
            "關於遠方誌 · 遠方誌", "遠方誌的編輯方式、查證標準與內容聲明。", "/about/",
            "ABOUT", "關於遠方誌", "這份刊物是什麼，文章如何產生，以及我們如何對待證據。", ABOUT_BODY),
        "privacy/index.html": build_static_page(
            "隱私權說明 · 遠方誌", "遠方誌如何處理（以及不處理）讀者的資料。", "/privacy/",
            "PRIVACY", "隱私權說明", "本刊收集的資料、瀏覽器本機儲存，以及託管服務的角色。", PRIVACY_BODY),
        "404.html": build_404(),
    }
    for idx in range(len(stories)):
        pages[f"articles/{stories[idx]['id']}/index.html"] = build_article(stories, idx)
    files = dict(pages)
    files["feed.xml"] = build_feed(stories)
    files["sitemap.xml"] = build_sitemap(stories, build_date)
    files["robots.txt"] = build_robots()

    dist = ROOT / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()
    for name in ASSETS:
        shutil.copy2(ROOT / name, dist / name)
    if (ROOT / "assets").is_dir():
        shutil.copytree(ROOT / "assets", dist / "assets")
    (dist / ".nojekyll").write_text("", encoding="utf-8")
    for rel, content in files.items():
        target = dist / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    # Sync the served files to the repository root as well: the root holds the
    # currently served site for local preview and for hosts that serve the
    # branch directly. dist/ stays the gh-pages artifact.
    for rel, content in files.items():
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    print(f"完成：驗證 {len(stories)} 篇文章，輸出 {len(files)} 個頁面與檔案至 dist/ 並同步到 repo 根目錄。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
