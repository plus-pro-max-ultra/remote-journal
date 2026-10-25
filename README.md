# 遠方誌｜把世界讀深一點

「遠方誌」是一份閱讀型知識刊物：以具體的故事或問題為入口，交代脈絡、機制、證據與反例，帶讀者理解世界背後的運作方式。

## 內容如何產生

文章由編輯流程直接撰寫與查證後加入 `content/articles/`，不依賴外部 AI API、排程產稿或任何付費服務。每篇稿件在加入正式內容前，依 `EDITORIAL_STANDARD.md` 與 `DAILY_PUBLISHING_CHECKLIST.md` 逐篇檢查：來源逐一開啟核對、數字與年代複查、區分事實與推論、附上反例或限制。

## 專案結構

- `index.html`：閱讀網站前端，支援分類、全文搜尋、隨機探索、收藏、個人反思與列印。
- `content/articles/*.json`：正式文章的唯一來源；新增或修改文章時編輯這裡，不要直接改 `stories.js`。
- `stories.js`：由建置腳本產生，讓網站可以直接於瀏覽器開啟。閱讀時間由建置時依實際篇幅計算。
- PWA 支援：部署到 HTTPS 後可安裝到主畫面；離線時可讀取已快取的內容，連線時一律取得最新文章。
- `ops/github-actions/`：預先寫好的 CI 與部署 workflows（目前停用，原因與啟用方式見 `ops/README.md`）。
- 部署現況：本機建置後推送 `gh-pages` 分支，由 GitHub Pages 從該分支發布。

## 本機預覽與重建

直接以瀏覽器開啟 `index.html` 即可閱讀。收藏與反思筆記儲存在該瀏覽器的本機儲存空間，不會跨裝置同步。

重建網站需要 Python 3.10 以上，無第三方套件：

```bash
python scripts/build_site.py
```

建置會驗證 `content/articles/`（必填欄位、重複 ID、HTTPS 來源、閱讀時間重算），更新 `stories.js`，並將公開網站輸出到 `dist/`。`dist/` 只含網站資產。

## 新增一篇文章

1. 依 `ARTICLE_TEMPLATE.md` 的骨架與 `EDITORIAL_STANDARD.md` 的標準撰寫，存為 `content/articles/00N-<id>.json`（使用 `sections` 純文字格式，網站會安全渲染）。
2. 執行 `python -m unittest discover -s tests -v` 與 `python scripts/build_site.py`，兩者皆須通過。
3. 推送 `main` 更新來源；再將建置產物推送 `gh-pages` 更新網站（細節見 `ops/README.md`）。

## 成本與安全

- 靜態網站無後端；GitHub Pages 公開儲存庫的費用與限制依官方方案為準。
- 內容流程不使用任何外部 AI API，沒有 API 金鑰或呼叫費用。
- 文章正文以純文字儲存、渲染時跳脫 HTML；不要把未審核的 HTML 放進內容資料。
