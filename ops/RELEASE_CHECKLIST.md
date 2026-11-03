# 正式上線檢查清單（architecture-v1 → main）

依 MM 指示設立：合併與上線前逐項核對，避免草稿內容或占位文字遺漏上線。

## 批准與合併

- [ ] 取得 MM 對本次更動的正式批准（分支不自行合併）。
- [ ] 決定合併目標：Option A（remote-journal 原地成為正式版）或 Option B（新的正式版 repo）。
- [ ] 合併前把分支更新到最新 main（每日出刊持續更新文章與 stories.js），重新執行 `python -m unittest discover -s tests` 與 `python3 scripts/build_site.py`。

## 上線前必須完成的替換

- [ ] `scripts/build_site.py` 頂端 `SITE_URL` 改為最終公開網址，重新建置（影響 canonical、og、sitemap、robots、feed）。
- [ ] 移除 `REVIEW_BANNER`（about/privacy 的「待 MM 核准」橫幅）。
- [ ] 以 MM 決定的版權人、年份與授權方式替換頁尾 `© 2026 遠方誌` 後的占位文字（`footer()`）。
- [ ] 補上 MM 決定的聯絡管道（`ABOUT_BODY` 與 `PRIVACY_BODY` 各一處）。
- [ ] 隱私權頁措辭經 MM 核准後，更新頁尾「本頁最後更新」日期。
- [ ] 若採 Option B，重新檢視頁尾措辭與「原型版」標示的處理。

## 部署後線上驗證

- [ ] 首頁、`/archive/`、任兩篇 `/articles/<slug>/`、`/about/`、`/privacy/` 均回 200 且內容完整。
- [ ] `/feed.xml`、`/sitemap.xml`、`/robots.txt` 可讀且網址正確。
- [ ] 舊連結 `#/story/<id>` 與 `#/archive` 正確轉址。
- [ ] 手機（390px）與桌面（1280px）截圖檢查；列印一篇文章確認列印樣式。
- [ ] service worker 更新為 v26 後，舊快取清除、離線可讀。
