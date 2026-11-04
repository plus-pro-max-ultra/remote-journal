## 2026-11-05

- 同步已批准 gh-pages 完整網站修改：頁首、頁面、001-017 代號與相容舊網址、收藏與筆記代號遷移。
- 017 最新修訂精確封存，兩站顯示品質控管，暫不開放閱讀；不加入正式刊出清單。
- 建置改為驗證並打包當前網站，避免舊模板覆寫直接修改；未發布 work-in-progress。

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
- 2026-11-04（MM 指示 phonemsg-01M6H8BXMJD2N346A2AZTMH2V1）：頁首品牌區加上方留白（標題不再近乎切頂）；首頁兩行標語改用明體系統字型堆疊（Songti TC／PMingLiU／Noto Serif CJK TC 等，無外部字體服務），第一行「世界不只發生。」放大加粗突出，第二行「它值得被理解。」大小維持原值（仍為主標題基準的 0.8 倍）。本機沙箱無明體字型，像素截圖僅驗證版面、尺寸與間距；明體實際字形需在 iOS／macOS 裝置上確認。
- 2026-11-04（MM 指示 phonemsg-01M6H980MPXCYW2SRZQEXFA656）：手機版「遠方誌」仍近乎切頂。原因：480px 斷點的舊規則把 topbar 上下留白設為 0，蓋過前次修正。現於 ≤480px 設 26px/16px、481-760px 設 30px/18px；桌機維持 14px/12px。實測 390px：品牌文字上緣距視窗頂 28px（修正前 2px）。
- 2026-11-04（MM 指示 phonemsg-01M6J366M7S0G430WXGY2MP90N，核准上線）：併入 MM 對關於頁與隱私頁的親修（134ebbc、9653f7a）並回填至建置來源；移除草稿橫幅、聯絡方式占位區塊（MM 已清空，尚無可公布管道，日後補回）與頁尾版權占位文字；頁尾保留「© 2026 遠方誌」。連同頂部留白／明體標語 UI 改善一併發布。
- 2026-11-04：頁尾對齊修正。原頁尾無水平留白、貼齊視窗邊緣，且首頁頁尾誤置於 .shell 內造成雙倍縮排；現頁尾與內文欄同寬同距（桌機 26px、手機 17px，全站一致），首頁頁尾移出 .shell。屬同批 UI 上線範圍（phonemsg-01M6J366M7S0G430WXGY2MP90N）。
- 2026-11-04（MM 指示 phonemsg-01M6JG9DFHVSRVHMGY10PCMH4D「主要是正式版不涉及github」）：正式網址定案為 https://journal-for-far.learnman.workers.dev；SITE_URL 自 GitHub Pages 改為正式網址，canonical、社群預覽、RSS 項目連結、sitemap、robots 與 404 資源位址一律指向正式版。隱私政策託管文字維持 MM 版本（Cloudflare Workers），不補回 GitHub 揭露。GitHub 鏡像維持運作，未刪除或改動。
