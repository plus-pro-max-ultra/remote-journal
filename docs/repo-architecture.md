# 遠方誌：編輯、預覽與正式發布 / Editing and releases

更新日期：2026-11-05。此文件取代整合前的多分支快照。

## 三個保留分支 / Three working roles

|分支|用途|誰在這裡編輯|
|---|---|---|
|`preview`|唯一工作來源：文章、草稿、頁面模板、樣式、設定與研究紀錄|在這裡修改並提交，不需等待預覽批准|
|`main`|Cloudflare 正式來源|只有對完整版本取得明確批准後才更新|
|`gh-pages`|由 preview 建置的 GitHub Pages 預覽產物|不是文章來源，不建議直接修改|

The single editing branch is `preview`. `main` is the approval-gated official edition. `gh-pages` contains generated preview files, not another set of article sources.

## 閱讀與編輯 / Read and edit

- 工作預覽：https://plus-pro-max-ultra.github.io/remote-journal/preview/
- 正式版：https://journal-for-far.learnman.workers.dev/
- 已刊文章來源：`content/articles/*.json`。
- 第017期待審稿：`drafts/017-antibiotic-course.json`。
- 十五篇待刊稿：`review/ready-drafts/*.json`。
- 圖片：`assets/img/`；共享樣式與互動：`assets/site.css`、`assets/site.js`。
- 關於、隱私及頁面結構來源：`scripts/build_site.py` 的模板。
- 選題：`content/topic-queue.json`；正式刊期紀錄：`ops/publication-ledger.json`。
- 研究、圖片授權與歷史檢核：`review/`。舊紀錄保留原貌，日期與狀態是當時的快照，不應取代目前規則。

在 GitHub 選擇 preview 分支，打開檔案、點鉛筆、編輯並提交。頁面本身沒有內建編輯器。儲存後會定期檢查並重建預覽；部署完成後才會顯示更新，不需批准。服務異常可能延遲部署，沒有即時或一小時上線保證。

Open the file on `preview`, edit with GitHub's pencil button and commit there. Periodic checks pick up changes and rebuild the preview; changes appear after deployment completes. There is no inline website editor or guaranteed deployment time.

## 來源與產出 / Sources and generated files

`python3 scripts/build_site.py` 驗證來源並產生 `dist/`，也同步產生的網站至儲存庫根目錄。測試另執行 `python3 -m unittest discover -s tests`，JavaScript 檢查為 `python3 scripts/check_inline_js.py`。建置並不取代這些獨立測試。

根目錄 HTML、文章頁、RSS、網站地圖是建置產物，重建會改寫。若直接修改這些檔案，須先核對差異並回填來源／模板，再重建；不能讓修改被舊來源覆蓋。gh-pages 上的直接修改也先回收，不會盲目覆蓋。

The build validates source content and generates `dist/` plus root website files. Run tests separately. Direct edits to generated HTML must be reconciled into the sources before rebuilding. Check both preview-source changes and direct gh-pages changes before deploying.

## 批准後如何更新正式版 / Promotion after approval

以批准範圍內的最新完整 preview 版本為準，逐項核對文章、其他頁面、樣式、設定及直接編輯；不是只搬文章，也不是從舊本地檔還原。產出與來源必須一致。批准後若有新差異，按實際批准範圍判斷：範圍內例行執行修正不另加關卡，超出範圍的實質更動才重新報准。

`main` 的變動會觸發 Cloudflare 正式建置與部署，不是儲存草稿。此次分支收攏沒有更新 main，也沒有批准正式刊出任何待審稿。審閱稿不放進正式刊期、RSS 或 sitemap；未決日期及期號不為了通過格式檢查而虛構。

An approved release carries the full approved preview version, including edits outside the articles. Reconcile generated and source edits. Only substantive changes beyond the actual approval scope need renewed approval. Any main change triggers production build/deploy. Consolidation is not a production release.

## 歷史保存 / Retired history

五個舊工作分支不再作編輯入口；各自的最後提交以 `archive/2026-11-05/<branch-name>` 標籤保留，對應清單見 `docs/branch-consolidation.json`。十五篇及017的文章／圖片已逐檔核對，研究紀錄見 `docs/research-records-manifest.json`，可用 SHA-256 驗證。

The five retired branches remain recoverable through archive tags. Research records retain their original bytes; the manifest records their source commits and hashes. Do not resume editing archived versions.

## 已知內容限制 / Source limitation

高鐵2011現地論文僅有已核讀的 HTTP 原文，HTTPS 入口憑證未能驗證。預覽保留真實書目與連結並標示限制，不讓來源消失或編號錯位；正式文章驗證器的 HTTPS 規則未放寬。朱鷺2015原論文已有可核讀的 PNAS HTTPS 連結。詳見 `review/depth-research/link-compatibility.md`。

The tunnel paper's verified original remains HTTP-only. Its preview citation is retained with a warning; this does not relax the published-article validator or claim the issue resolved.
