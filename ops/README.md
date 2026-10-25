# ops/ — 部署與維運說明

## 目前部署方式（gh-pages 分支）

網站以 GitHub Pages「從分支部署」（legacy build）運作：

- `main`：文章來源（`content/articles/*.json`）、建置腳本、測試與編輯文件。
- `gh-pages`：只放 `scripts/build_site.py` 的建置產物（靜態檔案），推送到此分支即觸發 Pages 建置。
- 公開網址：https://plus-pro-max-ultra.github.io/remote-journal/
- Pages 設定（Source = gh-pages / 根目錄）由帳號擁有者在 repo Settings 中一次完成；部署不需要再改設定。

每次發布的流程：

1. 更新 `content/articles/` 並依 `DAILY_PUBLISHING_CHECKLIST.md` 審核。
2. 執行測試、`python3 scripts/build_site.py`，再另行檢查 JavaScript 語法。
3. 推送 `main`（來源），再將 `dist/` 產物推送到 `gh-pages`（部署）。
4. 確認 Pages build 狀態為 built，並抽查線上網址。

## 為什麼不是 GitHub Actions 部署

目前發布權限無法修改 `.github/workflows/`；更新 Pages 設定的請求也遭拒。因此使用既有的 gh-pages 分支部署，不需擴大權限。這是實際遇到的權限限制，不是已驗證完整權限清單。


## 還原 GitHub Actions（未來如需要）

`ops/github-actions/` 保留了原本設計好的兩個 workflow：

- `check-content.yml`：push/PR 時驗證文章資料、重建網站、檢查 JS 語法。
- `deploy.yml`：push 到 main 後驗證並以 Actions 部署 Pages。


若未來要改用 Actions，需先確認工作流程檔案的修改權限，再把備份移回 `.github/workflows/`，並將 Pages 來源改為 GitHub Actions。

## 金鑰管理

- 不使用、不延伸任何其他專案（如單字系統）的 token 或 Secrets。

## 每日出刊（2026-10-25 起）

- 每篇流程：研究（所有關鍵主張對應實際開啟過的來源）→ 依 `EDITORIAL_STANDARD.md` 與 `DAILY_PUBLISHING_CHECKLIST.md` 審稿 → 測試與建置 → 推送 main 與 gh-pages → 線上與截圖驗證後才算完成。查證不足時延後並回報，不為連載降低品質。
- 網站功能補記（2026-10-25）：文章支援 `#/story/<id>` 深層連結；「下一篇」按鍵改為依刊號順序前進、最後一篇回到第一篇（修正原本依 related 跳轉會在部分文章間來回循環的問題）；手機版搜尋列「清除」按鈕不再直向換行。

每日出刊依據：MM 於 2026-10-25 指示現在開始每日出刊，並已要求專案與單字系統完全隔離。每個 Asia/Taipei 日期最多新增一篇；修改舊文不算新一期。

出刊日期以 `ops/publication-ledger.json` 為準；新一期發布且線上驗證成功後記錄日期、刊號及文章 ID。不要以舊文修訂時間代替出刊日。
