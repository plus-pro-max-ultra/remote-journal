# 從這裡開始：讓遠方誌上線

1. 在 GitHub 建立一個新的公開 repository（例如 `faraway-zine`），預設分支使用 `main`。
2. 將本專案全部檔案上傳至 `main`（包括 `content/`、`scripts/`、`tests/`、`.github/`）。
3. 開啟 repository 的 **Settings → Pages**，在 **Build and deployment → Source** 選擇 **GitHub Actions**。
4. 推送到 `main`（或在 Actions 手動執行 `Deploy Faraway Zine`）。成功後從部署結果取得公開網址。
5. 在手機瀏覽公開網站；可加入主畫面。收藏和筆記保存在該瀏覽器，不會跨裝置同步。

不需要任何 API 金鑰、Secrets 或額外設定。之後每篇新文章：加入 `content/articles/`、通過測試與建置、推送到 `main`，網站即更新。
