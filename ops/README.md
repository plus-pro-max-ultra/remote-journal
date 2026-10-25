# ops/ — 部署與維運說明

## 目前部署方式（gh-pages 分支）

網站以 GitHub Pages「從分支部署」（legacy build）運作：

- `main`：文章來源（`content/articles/*.json`）、建置腳本、測試與編輯文件。
- `gh-pages`：只放 `scripts/build_site.py` 的建置產物（靜態檔案），推送到此分支即觸發 Pages 建置。
- 公開網址：https://plus-pro-max-ultra.github.io/remote-journal/
- Pages 設定（Source = gh-pages / 根目錄）由帳號擁有者在 repo Settings 中一次完成；部署不需要再改設定。

每次發布的流程（由 Instinct 在本機執行）：

1. 更新 `content/articles/` 並依 `DAILY_PUBLISHING_CHECKLIST.md` 審核。
2. 本機跑測試與 `python3 scripts/build_site.py`（含 JS 語法檢查）。
3. 推送 `main`（來源），再將 `dist/` 產物推送到 `gh-pages`（部署）。
4. 確認 Pages build 狀態為 built，並抽查線上網址。

## 為什麼不是 GitHub Actions 部署

發布用的專用 fine-grained PAT（vault 項目「GitHub PAT remote-journal」）只有 remote-journal 單一 repo 的 Contents 讀寫權限，刻意不含 Workflows 與 Pages 設定權限（最小權限、與其他專案完全隔離）。GitHub 規定：推送涉及 `.github/workflows/` 的提交必須具備 Workflows 權限，因此 Actions 自動化暫時停用，改用上述分支部署。

## 還原 GitHub Actions（未來如需要）

`ops/github-actions/` 保留了原本設計好的兩個 workflow：

- `check-content.yml`：push/PR 時驗證文章資料、重建網站、檢查 JS 語法。
- `deploy.yml`：push 到 main 後驗證並以 Actions 部署 Pages。

若要啟用：帳號擁有者在同一個 token 上補加 repository 的 Workflows 權限（並在 vault 更新該項目），再把這兩個檔案移回 `.github/workflows/`，並將 Pages Source 改為 GitHub Actions 即可。

## 金鑰管理

- 部署只用 vault 中的「GitHub PAT remote-journal」，範圍僅此 repo。
- 不使用、不延伸任何其他專案（如單字系統）的 token 或 Secrets。
- token 不寫入 repo、不進 commit；每次部署由 Instinct 自 vault 複製到沙盒、用完即刪。

## 每日出刊（2026-10-25 起）

- 授權依據：MM 的 iMessage 核准 phonemsg-01M5QGTCVRZRMEE1CD315BAMYH（朝獨立維運方向進行、與單字系統完全隔離）、迭代授權 phonemsg-01M5QJWR6SEHX84TR5NHD20D8，以及每日出刊指示 phonemsg-01M5ST2TJFQMHBR9R46PNCQAEK（2026-10-25）。
- 節奏：每個台灣日期一篇。Instinct 每日喚醒後，以 `git log -1 --format=%cI -- content/articles/` 判斷今天是否已出刊；已出刊就跳過，避免跨午夜重複出刊。不對外承諾具體時刻。
- 每篇流程：研究（所有關鍵主張對應實際開啟過的來源）→ 依 `EDITORIAL_STANDARD.md` 與 `DAILY_PUBLISHING_CHECKLIST.md` 審稿 → 測試與建置 → 推送 main 與 gh-pages → 線上與截圖驗證後才算完成。查證不足時延後並回報，不為連載降低品質。
- 網站功能補記（2026-10-25）：文章支援 `#/story/<id>` 深層連結；「下一篇」按鍵改為依刊號順序前進、最後一篇回到第一篇（修正原本依 related 跳轉會在部分文章間來回循環的問題）；手機版搜尋列「清除」按鈕不再直向換行。
