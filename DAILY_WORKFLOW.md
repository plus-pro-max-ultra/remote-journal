# 上架當次同步觀察作者修改（MM 2026-11-22 21:05）

原訊息：phonemsg-01M81NS05WE81HCMQZ76PQZZZM，2026-11-22 21:05:23 Asia/Taipei。MM要求「觀察我的修改以增進修改策略」於上架時同時進行，以免遺漏。

- 每次gh審閱版或main正式版上架，都在同一次發布工作中，核對當下最新的作者修改、讀前後整段、整理對修改策略的調整，並納入該次發布結案。不延到下一篇備稿或另一個事後步驟。
- 備稿時的原有手改學習保留，但不能代替上架當次的現況核對。已就緒稿仍要在發布當下檢查比較版本是否更新；有新修改便重開相關對照與適用判斷。
- 依[上架同步學習檢查](editorial-learning/publication-checklist.md)記錄來源版本／比較範圍、實際修改或沒有新修改、明示偏好與編輯假設、策略處理及未解項；與部署、正文保留、像素和導覽驗證一起回報。
- 這是步驟的執行時點與結案要求，不新增改寫作者文字、變更事實意思、延後表訂日期或逐篇另問批准的權限。沒有新修改也如實記核對結果，不為填表硬造新教訓。
- 本規則向後適用。不得把新建的清單倒填成過去每次上架已完成的證明。

# 最新選題與段落要求（2026-11-21 21:17:56）

MM原訊息phonemsg-01M7Z438BFKFWZSC0BQ4YN9RF8：近日主題趨同，注意選題；段落須發展意旨，不要只有兩三句，楔子例外。

- 選題先比較近期正式刊、審閱稿與未刊候選的核心問題、角度與論述走向，不只換分類或地點。避免連續把不同對象都寫成傳統技藝、身體經驗與傳承困難。
- 每段先確定要讓讀者理解的一件事，再用必要的解釋、例子、因果或推論完成；不是把短段硬併，也不為湊句數填話。楔子可短，其他段落不能停在兩三句便跳到下一個小點。
- 這是後續寫作要求，不代表批准覆寫MM已手改文章或撤換已供審閱035。未上gh的036波浪導航撤回未排程研究，替代036以死信與公共服務例外處理為主；見research/unscheduled/2026-11-21-wave-piloting/UNSCHEDULED.md。

# 031正式發布新硬條件（MM2026-11-18 01:01）

原訊息phonemsg-01M7N7AAV9K7XPR56EG3MZ5ZA5：031正式上架前必須有符合文章敘述的實際照片，核清使用權並驗證像素。未滿足不得無照片照舊自動推main；若有延誤風險在08前報主對話。僅031，不以032示意圖替代。

# 視覺評估納入原有完稿檢查（2026-11-17補正）

- 研究計畫先寫本篇視覺任務，實際調查合適公開圖庫／開放館藏候選，核對原圖與授權，記錄採用或逐項不採用理由。不得只寫「不加裝飾圖」便結案。
- 使用[實際配圖評估流程](editorial-learning/visual-assessment.md)與[空白紀錄](editorial-learning/visual-assessment.template.json)，填本篇visual-assessment.json；查無合適候選亦保留真實查詢。未核清權利不採圖，不推成所有圖片不可用。
- 新稿032起跑`python scripts/check_draft_readiness.py daily/<issue>`，分別核對原有手改學習及視覺紀錄，缺項不稱完整ready。這不是新增張數配額、逐篇批准或另一套發布時間關卡，原有表訂日規則不變。無圖可以是完成評估後的合理結論。
- 已發布029／030與已供審閱031本次不動文章，不追認舊搜尋；031另記legacy_incomplete，誠實區分已部署與評估缺項。圖片載入測試對零張圖自動成功，僅能驗既有資產，不能替代本步驟。

# 完稿前的作者手改學習關卡（2026-11-17起）

1. 研究備稿前及宣告ready前，核對最新gh手改版本與原始回饋，讀變動段落前後文；保留作者全文，不從舊JSON還原。
2. 對照[潤飾準則](POLISHING_CRITERIA.md)與[已核實措辭例](editorial-learning/examples.md)，將新例分成明示偏好／編輯假設／待核錯字或事實。
3. 查核後重讀本篇全文，逐項判斷哪些教訓真的適用；在本篇editorial-learning-check.json記適用位置、原稿已有或實際改句、不適用理由、未解事項。不能只抄準則或強迫每項都改。
4. 僅詞句潤飾依既有授權處理；意思／事實變動先確認。完成後確認資料、範圍、來源與作者文字未被誤改，再跑HTML分行與像素檢查。
5. 執行`python scripts/check_editorial_learning.py daily/<issue>`檢查紀錄與檔案雜湊；它只檢查紀錄完整，不評自然程度。缺紀錄不得稱「完成手改學習驗收」。不能用填表取代全文判斷。
6. 發布前若gh或本篇稿件又變，重開相應檢查，不把舊的ready標記當最新證據；將新待決及期限風險如實交代，不能拿這個關卡取消表訂日自動發布規則。

以下發布規則仍適用；此關卡補足學習執行，不新增正式站改稿或其他帳號權限。

# 表訂日期自動正式發布（2026-11-09 22:44補充）

MM原訊息phonemsg-01M70C8H0Q4XD8AVX932SD6KHW：就是留給我一天的審閱期，不論我有沒有手動、要求修改都在文章表訂日期推到main上（但如果我完全沒有細調動作要另外提醒）。

這段取代下文所有未來逐篇main等待批准的舊規則。

- gh提前一天供審閱；文章表訂日期自動推main，無需另問批准。
- 保留gh所有最新手動修訂，處理已提出修改。沒有修訂／修改請求不是阻擋正式發布的理由。
- 若完全沒有細調動作，另外提醒MM。每次正式發布前查gh提交與原始對話，沒有證據時說明無法核實，不亂判沒有修改。
- 每早08:00前核實兩個結果：當天文章main＋翌日文章gh。例如11/10早023main、024（11/11稿）gh。
- 正式版不得混入未到表訂日期的下一篇，包含首頁／封存／feed／sitemap／隨機池。
- 實際上線時間、gh審閱日期與名義刊期分別記錄。

# 每日審閱稿提前一天

## 現行規則（2026-11-09 22:41）

MM原訊息 phonemsg-01M70C2RSV2NQS9KC3KMNC7481：以後遠方誌審閱版一律提早一天出到gh，以便有時間審稿。先把目前版推到main，然後現在先給出明天的稿子、明早給後天的以此類推。

- 11/9晚先發布批准的目前22篇到main，保留gh最新作者修訂、連結及隨機頁尾；之後才把11/10的023上gh，不混入這次main批准。
- 11/10早上給11/11的024；以後每早最晚08:00完成翌日新稿gh部署、核實及連結交付。
- 晚間備稿改為準備後天名義日期的稿件，翌晨提早一天發布gh。例如11/10晚準備11/12稿，11/11早發布。
- main仍逐次等原訊息批准；不能因名義刊期來到自動上正式版。
- 這是審閱提前，不是多算一期、倒填完成時間，實際gh發布日與稿件名義日期分開記。
- 06:00–06:15晨間執行、07:30–07:35期限風險檢查保留，目標均改為翌日稿。

以下為先前流程與沿用品質規則；若日期目標不一致以上述新規則為準。

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
