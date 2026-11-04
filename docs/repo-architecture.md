# 遠方誌 GitHub 倉庫架構說明 / Repository Architecture

Last verified: 2026-11-04, against the live remote. This document explains how the one repository is organized, how the two editions are published, and how editing works in practice.

## 1. One repository, everything inside

`plus-pro-max-ultra/remote-journal` (public) holds the articles, the build tooling, the site output, and the review material. Nothing content-related lives outside it.

https://github.com/plus-pro-max-ultra/remote-journal

## 2. Branches and their roles

| Branch | Role | State (2026-11-04) |
| --- | --- | --- |
| `main` | Source of truth: article data, build scripts, styles, tests, and the generated site | Live content through issue 016 |
| `gh-pages` | Publish-only branch for the GitHub Pages mirror | In sync with main's output |
| `content-readiness-2026-11-04` | Review branch: the fifteen revised manuscripts under `review/` | Awaiting MM review, unpublished |
| `daily-review-2026-11-04` | Review branch: issue 017 draft under `drafts/` | Awaiting MM review, unpublished |
| `architecture-v1` | Completed multi-page architecture work | Merged into main, kept as record |
| `photo-preview` | Older photo preview work | Inactive; can be deleted when MM wants |

Rules now in force: pushing to a review branch needs no approval. Moving anything onto `main` and the official edition requires MM's explicit approval. When a release is approved, the review branch's latest content, including MM's own edits, is what ships.

## 3. What lives where on `main`

- `content/articles/` - the 16 published articles, one JSON file each (text, sources, photos, date).
- `content/topic-queue.json` - the coming-week topic preview queue.
- `ops/publication-ledger.json` - the issue ledger: which article is which issue number and date.
- `ops/RELEASE_CHECKLIST.md` - the steps for a formal release.
- `ops/github-actions/` - reference copies of automation definitions only; no GitHub Actions run. All builds and checks run locally before anything is pushed.
- `scripts/build_site.py` - the build: validates every article JSON (including a required `YYYY-MM-DD` date), runs the content tests in `tests/`, regenerates the whole site into `dist/`, and syncs it to the repository root.
- `assets/site.css`, `assets/site.js` - shared styles and browser behavior.
- Repository root - the generated site itself: `index.html`, `about/`, `privacy/`, `archive/`, `articles/<slug>/`, `feed.xml`, `sitemap.xml`, `robots.txt`, `404.html`, `sw.js`, icons. These files are rebuilt from the sources above, so the root always matches the build.

## 4. The two editions

- Official edition: https://journal-for-far.learnman.workers.dev/ - a Cloudflare Workers project connected to this repository. Every push to `main` triggers an automatic build and deploy (deploy command `npx wrangler deploy`). Canonical links, RSS, sitemap and social previews all use this address.
- GitHub Pages mirror: https://plus-pro-max-ultra.github.io/remote-journal/ - serves the `gh-pages` branch. Updated by the agent as part of an approved release. Its pages point readers and search engines at the official edition.

## 5. How editing works, and what is safe to edit

MM can edit directly on GitHub's web interface or any git tool, on any branch.

Safe to edit directly (these are sources; a rebuild will not erase them):

- `content/articles/*.json` - article text, sources, photo choices.
- `content/topic-queue.json` - topic preview.
- `scripts/build_site.py` - the About and Privacy page text lives here as templates (`ABOUT_BODY`, `PRIVACY_BODY`), plus shared page structure.
- `ops/`, `docs/`, markdown files.

Regenerated on build (edit with care): the HTML at the repository root (`index.html`, `about/index.html`, `privacy/index.html`, `articles/*/index.html`, `feed.xml`, `sitemap.xml`). Direct edits here work, but the next build would overwrite them. The established practice, used for MM's 2026-11-04 About/Privacy edits: MM edits the generated file, the agent ports the same wording into the build source before rebuilding, then diffs the rebuilt output against MM's version to prove nothing was lost.

## 6. Feasibility, verified in practice on 2026-11-04

- MM edited `about/index.html` and `privacy/index.html` through the GitHub web UI on a branch; the changes merged cleanly with the agent's local work and shipped the same day.
- Two full release cycles ran end to end: branch push, merge to main, GitHub Pages deploy, and automatic Cloudflare Workers build. Both Workers builds succeeded.
- The content validator gates every build: 16 of 16 articles validated, all content tests pass.
- The daily and batch review branches were pushed and read back through the GitHub API to confirm the remote content matches.

Known notes, none blocking: the old `remote-journal` Worker connection in the Cloudflare dashboard no longer exists and its preview builds will keep failing harmlessly until MM disconnects it; branch preview builds only run when a branch is pushed (enabling the setting does not rebuild older pushes); issue numbers and dates come from `ops/publication-ledger.json`, so a new article enters the site by adding its JSON plus a ledger entry on a review branch.

---

# 倉庫架構（繁體中文）

以下為 2026-11-04 對線上倉庫實際查核後的說明。

## 1. 單一倉庫

所有文章、建置工具、網站輸出與審閱資料都在 `plus-pro-max-ultra/remote-journal`（公開）這一個倉庫裡。

## 2. 分支角色

| 分支 | 角色 | 狀態（2026-11-04） |
| --- | --- | --- |
| `main` | 唯一正式來源：文章資料、建置腳本、樣式、測試與產生的網站 | 已刊至第 016 期 |
| `gh-pages` | 僅供發布的 GitHub Pages 鏡像分支 | 與 main 輸出同步 |
| `content-readiness-2026-11-04` | 審閱分支：十五篇重修稿，放在 `review/` | 待你審閱，未發布 |
| `daily-review-2026-11-04` | 審閱分支：第 017 期草稿，放在 `drafts/` | 待你審閱，未發布 |
| `architecture-v1` | 已完成的多頁架構工作 | 已併入 main，保留紀錄 |
| `photo-preview` | 早期照片預覽工作 | 停用中；你要清理時可刪 |

現行規則：推送到審閱分支不需批准；推上 `main` 與正式版才需要你明確批准。批准上線時，以審閱分支的最新內容為準，包含你做的修改。

## 3. `main` 裡的內容位置

- `content/articles/`：16 篇已刊文章，每篇一個 JSON（內文、來源、照片、日期）。
- `content/topic-queue.json`：未來一週預告的選題佇列。
- `ops/publication-ledger.json`：出刊紀錄，登載哪一篇是第幾期、哪一天。
- `ops/RELEASE_CHECKLIST.md`：正式發布步驟。
- `ops/github-actions/`：自動化定義的參考副本，沒有實際跑 GitHub Actions；所有建置與檢查都在本機完成後才推送。
- `scripts/build_site.py`：建置程式。驗證每篇 JSON（日期 `YYYY-MM-DD` 為必填）、跑 `tests/` 的內容測試、把整個網站重新產生到 `dist/` 並同步到倉庫根目錄。
- `assets/site.css`、`assets/site.js`：全站共用樣式與瀏覽器行為。
- 倉庫根目錄：產生的網站本體（`index.html`、`about/`、`privacy/`、`archive/`、`articles/`、`feed.xml`、`sitemap.xml`、`robots.txt`、`404.html`、`sw.js` 與圖示）。這些由上述來源重建，根目錄永遠與建置結果一致。

## 4. 兩個版本

- 正式版：https://journal-for-far.learnman.workers.dev/ ，Cloudflare Workers 專案連接此倉庫。每次推送 `main` 會自動建置並部署（部署指令 `npx wrangler deploy`）。標準網址、RSS、網站地圖與分享預覽都用這個網址。
- GitHub Pages 鏡像：https://plus-pro-max-ultra.github.io/remote-journal/ ，服務 `gh-pages` 分支，批准發布時由我更新。其頁面會把讀者與搜尋引擎導向正式版。

## 5. 你的編輯方式與安全範圍

你可以在 GitHub 網頁或任何 git 工具上直接編輯任何分支。

可以直接改（屬於來源，重建不會洗掉）：

- `content/articles/*.json`：文章內文、來源、照片。
- `content/topic-queue.json`：預告選題。
- `scripts/build_site.py`：關於頁與隱私頁的文字以模板形式在這裡（`ABOUT_BODY`、`PRIVACY_BODY`），以及共用頁面結構。
- `ops/`、`docs/` 與各 markdown 文件。

重建時會覆蓋（直接改有效，但下次建置會被覆寫）：根目錄的 HTML（`index.html`、`about/index.html`、`privacy/index.html`、`articles/*/index.html`、`feed.xml`、`sitemap.xml`）。既定做法（已用於你 2026-11-04 對關於頁／隱私頁的修改）：你改產生的檔案，我在重建前把同樣的文字回填到建置來源，重建後再與你的版本逐行比對，確認沒有遺失。

## 6. 可行性：2026-11-04 實際驗證

- 你透過 GitHub 網頁在分支上修改了關於頁與隱私頁，與我的工作合併無衝突，當天上線。
- 兩次完整發布流程實際跑完：分支推送、併入 main、GitHub Pages 部署、Cloudflare Workers 自動建置，兩次 Workers 建置都成功。
- 內容驗證器每次都把關：16 篇全部通過，內容測試全數通過。
- 每日與十五篇的審閱分支已推送，並透過 GitHub API 讀回確認雲端內容一致。

目前不影響操作的事項：Cloudflare 後台舊的 `remote-journal` 連線已不存在，它的預覽建置會繼續失敗但無害，你方便時可中斷連線；分支預覽只在新推送時觸發（開啟設定不會重建舊推送）；新文章靠「新增 JSON＋在 `ops/publication-ledger.json` 登記一期」進入網站，全部在審閱分支上完成。
