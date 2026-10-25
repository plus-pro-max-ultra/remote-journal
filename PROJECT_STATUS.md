# 遠方誌專案狀態

## 營運模式

內容由編輯流程直接撰寫、查證並加入正式內容，不使用外部 AI API 產稿；無 API 金鑰、Secrets、排程產稿 workflow 或相關費用。每篇依 `EDITORIAL_STANDARD.md` 與 `DAILY_PUBLISHING_CHECKLIST.md` 審核後刊出。

## 已完成

- [x] 文章內容與網站程式分離（`content/articles/*.json` 為唯一來源）。
- [x] 內容驗證與建置腳本；部署前檢查欄位、重複 ID 與 HTTPS 來源。
- [x] 首頁分類依文章動態產生；今日選讀按日期輪替既有文章。
- [x] 六篇文章：道路與誘發需求、平均數、皇位繼承、賣斷與存貨、地圖投影、海底電纜。
- [x] 正文以純文字區塊儲存、渲染時跳脫 HTML。
- [x] PWA：service worker 改為連線優先，新文章發布後回訪讀者可立即看到；離線時退回快取。
- [x] 閱讀時間依實際篇幅於建置時計算，不再手填。
- [x] 本機驗證：4 項測試通過、建置成功、JS 語法檢查通過。
- [x] 海底電纜一篇的全部 8 個來源均逐一開啟並核對其支持的主張。

## 已發布（2026-10-25）

- [x] 公開 repo：https://github.com/plus-pro-max-ultra/remote-journal
- [x] 公開網址：https://plus-pro-max-ultra.github.io/remote-journal/ （Pages 來源：gh-pages 分支）
- [x] 部署後於實際網址完成桌面（1280px）與手機（390px）截圖驗證；各資源 HTTP 200、service worker 為 v3 連線優先版本。

## 已知限制

- 收藏與反思筆記只存在各裝置的瀏覽器本機儲存，不跨裝置同步。
- 既有四篇早期樣稿（001–004）正文為受信任的 HTML 格式；新文章一律使用純文字 `sections` 格式。
- 部署採 gh-pages 分支發布而非 GitHub Actions：專用 token 刻意不含 Workflows／Pages 設定權限（最小權限、專案隔離）。原設計的 Actions workflows 保留於 `ops/github-actions/`，啟用方式見 `ops/README.md`。
