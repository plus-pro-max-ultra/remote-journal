# 每日新刊交付

2026-11-06 23:23，MM原訊息：以後每日出刊改為最晚早上八點。適用台北日期；新刊先到gh工作預覽，正式main仍須依原規則批准。

## 交付與準備分開

- 每日新一期最晚08:00在gh完成部署、核實閱讀頁與手機／桌機畫面，再由主對話交付連結。
- 前晚19:00–20:00啟動次日選題、讀來源、查核、成稿與全文潤飾。窗口是準備時間，不是新的交付時間。
- 當日06:00–06:15接續未完成工作，發布gh並核實。不可把「已有草稿」算作完成，也不能僅推送後就結案。
- 07:30–07:35安全檢查：若仍未核實完成，立即回報實際階段與期限風險，繼續執行；品質不足則延後，不低標趕刊，也不等08:00後才告知。
- 規則建立當晚已過例行前晚時間，因此為11/7另設11/6 23:40–23:50備稿接續。這不是再做一篇11/6。

## 防止重複與假完成

核對WIP daily、實際gh、部署與正式ledger。舊文修訂與較早備稿的confirmed_batch正式轉移不算當日新刊。跨午夜未完成工作保留原目標日與真實實際上線時間，不能倒填當成準時出刊。

完成一個日期的新刊後，接著準備下一日期；不得讓既有修訂或15篇未刊稿全文潤飾再次擠掉每日責任。15篇稿仍留在WIP，與每日新稿分開，不因排程改動自動刊出。

22:00例行夜間網站檢查若包含當日文章，檢查當日早上已刊出的那篇。網站檢查不取代次日研究備稿；其時間由主對話另行協調，不在本次擅改。

## 本次接續

11/6獨立019肖維洞研究／稿件：daily/2026-11-06-chauvet-dating。它不是11/7新刊。001–018正式main已核實，新稿019的main發布仍須另行批准。

## 空檔工作

11/6 23:43 MM另指示「運算有空閒時就可以進行主題研究或進行目前系統的任何檢查」。實際有空檔時，補未來主題研究或有意義的系統檢查，留下可追溯來源與進度；不能擠掉進行中的每日新刊及08:00期限，不為製造進度重複查詢，也不增加正式發布、花費或帳戶權限。原訊息phonemsg-01M6RRF5CWMH1DFKBFEWBWHF08。

## Article links and random footers (MM 2026-11-09 11:58)

- User instruction: 連結加入（gh)、頁尾的按鍵設定成在所有文章中隨機跳轉（對於所有文章）.
- gh implementation:193dc9f + binding fix1bac328. All existing article footers use `data-surprise`, label 隨機讀一篇 and heading 隨機探索另一篇文章, fallback `../../archive/` without JavaScript. Copy the current footer pattern for every new article, not an old next-story link.
- Shared `assets/site.js` binds every `[data-surprise]` button, including header and footer. Article fallback pool comes from all numbered values in `ARTICLE_ID_ALIASES`, deduplicated and excluding the current canonical ID. Keep the registry current when adding an issue so all articles can reach it. Do not use only visible home cards for an article footer.
- Check actual footer clicks, not merely label/DOM appearance. Verify every current article reaches a different valid article. Deterministic pool tests should cover all eligible targets; use direct numbered paths, not alias intermediate pages.
- New links must help explain the current question or offer a precise contrast; no link quota. Nov9 approved links:006→002/001,004→002,010↔018. Weaker review options are not approved;022→006 comparison withdrawn.
- This instruction was executed on gh only. Formal main has its own approved article set; a future authorized main release must not import019/022 or include unapproved articles in its random pool.
