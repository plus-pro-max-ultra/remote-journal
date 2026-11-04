# 遠方誌 Pages 工作預覽

`gh-pages` 是 MM 的可直接編輯版本。GitHub Pages 讀取本分支根目錄，修改實際 HTML、CSS、JS 後，待 Pages 部署完成才會顯示，不是即時儲存即上線。

- `index.html`：首頁。
- `articles/<文章代號>/index.html`：各篇文章頁。
- `about/index.html`、`privacy/index.html`：其他頁面。
- `assets/site.css`、`assets/site.js`：共用樣式及互動。
- `stories.js`：首頁等功能用的文章資料；變更相關文章標題／摘要時，須核對此處與文章頁一致。

本分支的實際網站檔案是預覽版本的依據。沒有 preview → gh-pages 的重建覆寫作業，也沒有會把 JSON／Python 模板自動轉成頁面的工作流程。改某一份 HTML 不會自動同步其他頁面；跨頁修改要核對全部受影響的檔案。

未完成材料只放 `work-in-progress`，完成後可整合回此預覽。`main` 是正式網站，仍須 MM 明確批准；批准後要比較完整版本，包含 MM 直接編輯的文字、頁面、樣式與設定，不能只搬文章或用舊模板覆蓋。

舊來源／模板／測試與舊網站均保存在 `archive/2026-11-05/preview-before-single-pages` 及 `archive/2026-11-05/gh-pages-before-single-pages` 標籤。若須使用舊工具，先將本分支的直接修改帶回來源、對照全部差異後再產生；不得盲目重建。
