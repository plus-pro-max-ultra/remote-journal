# 更動日誌

依 MM 2026-11-04 指示：所有更動先到分支，正式轉移到 main 必須經過正式批准；分支上的更新逐筆記錄於此，避免正式上線時有所遺漏。

## architecture-v1（2026-11-04，依架構調整計畫 v1.0）

- 每篇文章 JSON 加入 `date` 出刊日期欄位（007-016 依 `ops/publication-ledger.json`；001-007 首發日 2026-10-25）。建置與測試改為必填 `YYYY-MM-DD`。
- `scripts/build_site.py` 重寫：每次建置輸出真正的獨立頁面：首頁、`archive/`、`articles/<slug>/`（16 篇）、`about/`、`privacy/`、`404.html`，外加 `sitemap.xml`、`robots.txt`、`feed.xml`；輸出至 `dist/` 並同步 repo 根目錄（沿用既有慣例，供本機預覽與直接服務分支的託管使用）。
- 樣式抽至 `assets/site.css`（原 `index.html` 內嵌樣式原樣搬遷，另加新規則）；互動腳本抽至 `assets/site.js`。
- 導覽改為一般連結；JavaScript 只做增強（搜尋、篩選、收藏、筆記、未來一週預告、隨機探索）。舊 `#/story/<id>` 與 `#/archive` 連結自動轉址到新頁面。
- 移除「更新內容」按鈕；「最新刊期」改為純文字（計畫預設 4）。service worker 維持連線優先（CACHE_NAME v25 → v26），並在讀者回到分頁時靜默檢查更新，不在閱讀中途重整。
- 文章頁顯示出刊日期、不署名（計畫預設 3）；「複製文章標題」改為「複製文章連結」（每篇文章現在有真正的網址）。
- RSS：`feed.xml`（RSS 2.0，每篇一個 item，含標題、連結、出刊日期、摘要），每頁 head 與頁尾均有入口。
- 新增 `content/topic-queue.json`：`TOPIC_QUEUE` 自 `index.html` 遷入，出刊流程改為編輯此檔；首頁預告於建置時產生，瀏覽器端再依當日日期重算。
- `about/`、`privacy/` 為草稿頁，頁首有「待 MM 核准」橫幅（`REVIEW_BANNER`），聯絡方式與版權聲明為待確認占位文字；正式上線前依 `ops/RELEASE_CHECKLIST.md` 移除。
- 頁尾不再標示「原型版」（正式版架構工作的一部分；若最終採新 repo 方案，於檢視時再確認措辭）。
- 文章索引改為完整靜態清單（依月份分組），取消 JS 分頁；搜尋、領域與月份篩選保留。
- 首發文章的「首發」標註移除，統一顯示出刊日期（計畫預設 1）。
- 絕對網址（canonical、社群預覽、sitemap、feed）暫用現行 GitHub Pages 網址；最終網址確定後改 `scripts/build_site.py` 頂端 `SITE_URL` 一處即可（見 release checklist）。
- 2026-11-04：推送本筆無內容更動，觸發 Cloudflare Workers Builds 對 architecture-v1 的預覽建置（依官方文件，非 production 分支的推送會產生獨立 Preview，不影響正式站）。網站內容與程式無任何變更。
