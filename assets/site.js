// Generated-site enhancements. Every page works without JavaScript; this file
// adds search, filters, favorites, notes, the topic preview and offline
// updates on top of the static pages.
(function () {
  "use strict";
  var ROOT = document.body.getAttribute("data-root") || "./";

  // Numbered identifiers retain existing bookmarks, favorites and notes.
  var ARTICLE_ID_ALIASES = {"roads":"001-roads","median":"002-median","imperial":"003-imperial","stock":"004-stock","maps":"005-maps","submarine-cables":"006-submarine-cables","webb-l2":"007-webb-l2","smallpox":"008-smallpox","comet-windows":"009-comet-windows","daylight-saving-time":"010-daylight-saving-time","typhoon-names":"011-typhoon-names","power-frequency":"012-power-frequency","runway-numbers":"013-runway-numbers","escalator-stand-walk":"014-escalator-stand-walk","movie-popcorn":"015-movie-popcorn","survivorship-bias":"016-survivorship-bias","antibiotic-course":"017-antibiotic-course","seven-day-week":"018-seven-day-week","chauvet-dating":"019-chauvet-dating","river-personhood":"020-river-personhood","kilogram":"021-kilogram","check-digits":"022-check-digits","leap-seconds":"023-leap-seconds"};
  function currentId(id) { return ARTICLE_ID_ALIASES[id] || id; }
  try {
    var savedIds = JSON.parse(localStorage.getItem("faraway-saved") || "[]");
    if (Array.isArray(savedIds)) {
      var migrated = savedIds.map(currentId).filter(function (v, i, a) { return a.indexOf(v) === i; });
      localStorage.setItem("faraway-saved", JSON.stringify(migrated));
    }
    Object.keys(ARTICLE_ID_ALIASES).forEach(function (oldId) {
      var newKey = "faraway-note-" + ARTICLE_ID_ALIASES[oldId];
      var oldNote = localStorage.getItem("faraway-note-" + oldId);
      if (oldNote !== null && localStorage.getItem(newKey) === null) localStorage.setItem(newKey, oldNote);
    });
  } catch (e) { }

  var PAGE = document.body.getAttribute("data-page") || "";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function toast(text) {
    var t = $("#toast"); if (!t) return;
    t.textContent = text; t.classList.add("show");
    clearTimeout(window.__toastT);
    window.__toastT = setTimeout(function () { t.classList.remove("show"); }, 2100);
  }
  function getSaved() { try { return JSON.parse(localStorage.getItem("faraway-saved") || "[]"); } catch (e) { return []; } }
  function setSaved(a) { try { localStorage.setItem("faraway-saved", JSON.stringify(a)); } catch (e) { toast("此瀏覽環境無法儲存收藏，請改用一般瀏覽器開啟。"); } }
  function getNote(id) { try { return localStorage.getItem("faraway-note-" + id) || ""; } catch (e) { return ""; } }
  function setNote(id, v) { try { localStorage.setItem("faraway-note-" + id, v); } catch (e) { } }

  // Offline support: register the service worker, and silently re-check for
  // updates when the reader returns to the tab (the running page is never
  // reloaded mid-read; the new issue appears on the next navigation).
  if ("serviceWorker" in navigator && location.protocol.indexOf("http") === 0) {
    navigator.serviceWorker.register(ROOT + "sw.js", { updateViaCache: "none" }).then(function (reg) {
      document.addEventListener("visibilitychange", function () {
        if (!document.hidden) { try { reg.update(); } catch (e) { } }
      });
    }).catch(function () { });
  }

  // Legacy hash links keep working: #/story/<slug> and #/archive redirect to
  // the real pages.
  function hashRedirect() {
    var m = location.hash.match(/^#\/story\/([A-Za-z0-9_-]+)/);
    if (m) { location.replace(ROOT + "articles/" + currentId(m[1]) + "/"); return true; }
    if (location.hash === "#/archive") { location.replace(ROOT + "archive/"); return true; }
    return false;
  }
  if (PAGE === "home" || PAGE === "404") {
    hashRedirect();
    window.addEventListener("hashchange", hashRedirect);
  }

  function setupSurprise() {
    $$("[data-surprise]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var ids = $$(".article-card[data-id]").map(function (c) { return c.getAttribute("data-id"); });
      if (!ids.length && window.FARAWAY_STORIES) ids = window.FARAWAY_STORIES.map(function (s) { return s.id; });
      // Article footers use the complete, current numbered collection, not
      // the cards visible on a page. New issues update this shared registry.
      if (!ids.length) ids = Object.keys(ARTICLE_ID_ALIASES).map(function (key) { return ARTICLE_ID_ALIASES[key]; });
      var current = currentId(document.body.getAttribute("data-id"));
      var pool = ids.map(currentId).filter(function (x, i, all) { return x !== current && all.indexOf(x) === i; });
      if (!pool.length) { location.href = btn.getAttribute("href"); return; }
      var pick = pool[Math.floor(Math.random() * pool.length)];
      location.href = ROOT + "articles/" + pick + "/";
    });
    });
  }
  setupSurprise();

  // ---------------- home ----------------
  if (PAGE === "home") {
    var cards = $$(".article-card[data-id]");
    var grid = $("#articleGrid");
    var state = { filter: "all", q: "", savedOnly: false };
    var saved = getSaved();

    function updateSavedCount() { var el = $("#savedCount"); if (el) el.textContent = getSaved().length; }
    updateSavedCount();

    function isDefault() { return state.filter === "all" && !state.q && !state.savedOnly; }
    function matches(c) {
      if (state.filter !== "all" && c.getAttribute("data-cat") !== state.filter) return false;
      if (state.q && c.getAttribute("data-search").indexOf(state.q) === -1) return false;
      if (state.savedOnly && getSaved().indexOf(c.getAttribute("data-id")) === -1) return false;
      return true;
    }
    function render() {
      var filtering = !isDefault();
      grid.classList.toggle("filtering", filtering);
      var shown = 0;
      cards.forEach(function (c) {
        var ok = !filtering || matches(c);
        c.classList.toggle("filter-show", filtering && ok);
        if (!filtering) c.classList.remove("filter-show");
        if (filtering && ok) shown++;
      });
      var title = $("#archiveTitle");
      if (title) title.textContent = state.savedOnly ? "我的收藏" : (filtering ? "搜尋與篩選結果" : "最新文章");
      var feat = $("#featureGrid"); if (feat) feat.style.display = filtering ? "none" : "";
      var more = $("#viewAllWrap"); if (more) more.style.display = filtering ? "none" : "";
      var empty = $("#emptyResult");
      if (empty) empty.style.display = (filtering && shown === 0) ? "" : "none";
      if (state.savedOnly) updateSavedCount();
    }
    // category chips
    var cats = [];
    cards.forEach(function (c) { var k = c.getAttribute("data-cat"); if (cats.indexOf(k) === -1) cats.push(k); });
    cats.sort(function (a, b) { return a.localeCompare(b, "zh-Hant"); });
    var fbox = $("#filters");
    if (fbox) {
      fbox.innerHTML = "";
      var all = document.createElement("button");
      all.className = "chip active"; all.setAttribute("data-filter", "all"); all.textContent = "全部探索";
      fbox.appendChild(all);
      cats.forEach(function (c) {
        var b = document.createElement("button");
        b.className = "chip"; b.setAttribute("data-filter", c); b.textContent = c;
        fbox.appendChild(b);
      });
      fbox.addEventListener("click", function (e) {
        var b = e.target.closest("[data-filter]"); if (!b) return;
        state.filter = b.getAttribute("data-filter");
        $$(".chip", fbox).forEach(function (x) { x.classList.toggle("active", x === b); });
        render();
      });
    }
    var si = $("#searchInput");
    if (si) si.addEventListener("input", function () { state.q = si.value.trim().toLowerCase(); render(); });
    var cs = $("#clearSearch");
    if (cs) cs.addEventListener("click", function () { si.value = ""; state.q = ""; state.filter = "all"; state.savedOnly = false; render(); });
    var sn = $("#savedNav");
    if (sn) sn.addEventListener("click", function () {
      state.savedOnly = !state.savedOnly;
      if (state.savedOnly) { state.filter = "all"; state.q = ""; if (si) si.value = ""; }
      render();
      window.scrollTo({ top: 0, left: 0, behavior: "instant" });
    });

    // topic preview: recompute from today's date in the reader's timezone so a
    // stale build never shows yesterday's queue.
    function taipeiTodayStr() { return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Taipei", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date()); }
    function addDaysStr(dstr, n) { var d = new Date(dstr + "T12:00:00+08:00"); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
    function weekdayZh(dstr) { return "日一二三四五六"[new Date(dstr + "T12:00:00+08:00").getUTCDay()]; }
    function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
    function renderTopics() {
      var box = $("#previewTopics");
      if (!box || !window.FARAWAY_TOPICS || !window.FARAWAY_STORIES) return;
      var stories = window.FARAWAY_STORIES;
      var taken = {};
      stories.forEach(function (s) { if (s.date) taken[s.date] = true; });
      var today = taipeiTodayStr();
      var queue = window.FARAWAY_TOPICS.filter(function (t) { return !stories.some(function (s2) { return s2.id === t.id; }); });
      var dates = []; var i = taken[today] ? 1 : 0;
      while (dates.length < 7 && i < 40) { dates.push(addDaysStr(today, i)); i++; }
      var byDate = {};
      queue.forEach(function (t) { if (t.date >= today) byDate[t.date] = t; });
      var rows = [];
      queue.filter(function (t) { return t.date < today; }).sort(function (a, b) { return a.date < b.date ? -1 : 1; })
        .forEach(function (t) { rows.push({ date: t.date, topic: t, delayed: true }); });
      queue.forEach(function (t) { if (t.date >= today && taken[t.date] && dates.indexOf(t.date) !== -1) rows.push({ date: t.date, topic: t, delayed: true }); });
      dates.forEach(function (d) { rows.push({ date: d, topic: byDate[d] || null, delayed: false }); });
      box.innerHTML = rows.map(function (r) {
        var dateLabel = (r.delayed ? "原定 " : "") + r.date + "（" + weekdayZh(r.date) + "）";
        if (!r.topic) {
          return '<div class="topic-row preview"><span class="topic-meta-line"><span class="topic-num">候選</span><span class="topic-date">' + esc(dateLabel) + '</span><span class="topic-cat">研擬中</span></span><span class="topic-title" style="color:var(--muted)">題目確認後公布 <span class="topic-badge">預告</span></span></div>';
        }
        var t = r.topic;
        return '<div class="topic-row preview"><span class="topic-meta-line"><span class="topic-num">候選</span><span class="topic-date">' + esc(dateLabel) + '</span><span class="topic-cat">' + esc(t.category) + '</span></span><span class="topic-title">' + esc(t.title) + ' <span class="topic-badge">' + (r.delayed ? "順延・研究中" : "預告・研究中") + "</span></span></div>";
      }).join("");
    }
    renderTopics();
  }

  // ---------------- archive ----------------
  if (PAGE === "archive") {
    var rows = $$(".topic-row[data-id]");
    var heads = $$(".month-head[data-mh]");
    var astate = { filter: "all", q: "", month: "all" };
    function arender() {
      var shown = 0;
      rows.forEach(function (r) {
        var ok = true;
        if (astate.month !== "all" && r.getAttribute("data-month") !== astate.month) ok = false;
        if (astate.filter !== "all" && r.getAttribute("data-cat") !== astate.filter) ok = false;
        if (astate.q && r.getAttribute("data-search").indexOf(astate.q) === -1) ok = false;
        r.style.display = ok ? "" : "none";
        if (ok) shown++;
      });
      heads.forEach(function (h) {
        var any = rows.some(function (r) { return r.getAttribute("data-month") === h.getAttribute("data-mh") && r.style.display !== "none"; });
        h.style.display = any ? "" : "none";
      });
      var count = $("#archiveCount");
      if (count) count.textContent = shown ? ("共 " + shown + " 篇") : "";
      var empty = $("#archiveEmpty");
      if (empty) empty.style.display = shown === 0 ? "" : "none";
    }
    var acats = [];
    rows.forEach(function (r) { var k = r.getAttribute("data-cat"); if (acats.indexOf(k) === -1) acats.push(k); });
    acats.sort(function (a, b) { return a.localeCompare(b, "zh-Hant"); });
    var af = $("#archiveFilters");
    if (af) {
      af.innerHTML = "";
      var aall = document.createElement("button");
      aall.className = "chip active"; aall.setAttribute("data-afilter", "all"); aall.textContent = "全部探索";
      af.appendChild(aall);
      acats.forEach(function (c) {
        var b = document.createElement("button");
        b.className = "chip"; b.setAttribute("data-afilter", c); b.textContent = c;
        af.appendChild(b);
      });
      af.addEventListener("click", function (e) {
        var b = e.target.closest("[data-afilter]"); if (!b) return;
        astate.filter = b.getAttribute("data-afilter");
        $$(".chip", af).forEach(function (x) { x.classList.toggle("active", x === b); });
        arender();
      });
    }
    var asi = $("#archiveSearchInput");
    if (asi) asi.addEventListener("input", function () { astate.q = asi.value.trim().toLowerCase(); arender(); });
    var ac = $("#archiveClear");
    if (ac) ac.addEventListener("click", function () { asi.value = ""; astate.q = ""; astate.filter = "all"; astate.month = "all"; var ms = $("#archiveMonthSelect"); if (ms) ms.value = "all"; arender(); });
    var ams = $("#archiveMonthSelect");
    if (ams) ams.addEventListener("change", function () { astate.month = ams.value; arender(); });
  }

  // ---------------- article ----------------
  if (PAGE === "article") {
    // Citation markers jump into the sources block: open the details first.
    document.addEventListener("click", function (e) {
      var a = e.target.closest("sup.cite a");
      if (!a) return;
      e.preventDefault();
      var li = document.querySelector(a.getAttribute("href"));
      if (!li) return;
      var d = li.closest("details");
      if (d && !d.open) d.open = true;
      li.scrollIntoView({ behavior: "auto", block: "center" });
      setTimeout(function () { li.scrollIntoView({ behavior: "auto", block: "center" }); }, 700);
    });
    var id = document.body.getAttribute("data-id");
    var bm = $("#bookmarkBtn");
    function paintBm() {
      var on = getSaved().indexOf(id) !== -1;
      bm.textContent = on ? "✓ 已收藏" : "＋ 收藏這篇";
      bm.classList.toggle("saved", on);
    }
    if (bm) {
      paintBm();
      bm.addEventListener("click", function () {
        var a = getSaved();
        if (a.indexOf(id) !== -1) a = a.filter(function (x) { return x !== id; }); else a.push(id);
        setSaved(a); paintBm();
        toast(a.indexOf(id) !== -1 ? "已加入收藏" : "已從收藏移除");
      });
    }
    var pb = $("#printBtn");
    if (pb) pb.addEventListener("click", function () {
      $$("details.srcblk").forEach(function (d) { d.open = true; });
      window.print();
    });
    window.addEventListener("beforeprint", function () { $$("details.srcblk").forEach(function (d) { d.open = true; }); });
    var cl = $("#copyLinkBtn");
    if (cl) cl.addEventListener("click", function () {
      var title = document.title.replace(/ · 遠方誌.*$/, "");
      var url = location.href;
      function done() { toast("已複製文章連結"); }
      function fallback() {
        try {
          var ta = document.createElement("textarea");
          ta.value = url; document.body.appendChild(ta); ta.select();
          document.execCommand("copy"); document.body.removeChild(ta); done();
        } catch (e) { toast(url); }
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, fallback);
      else fallback();
    });
    var note = $("#reflectionNote");
    if (note) {
      note.value = getNote(id);
      note.addEventListener("input", function () { setNote(id, note.value); });
    }
  }
})();
