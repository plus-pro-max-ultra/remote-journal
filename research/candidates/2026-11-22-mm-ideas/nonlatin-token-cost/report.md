# 非拉丁文字的 AI token tax：候選研究簡報
2026-11-22，初步選題研究，未排期。

這題有可核對的技術與公平性問題：同義內容換一種語言，模型可能需要更多token；按token計費時，這可能增加費用，也可能減少同一context window能容納的內容。「tax」在已讀技術材料中是額外負擔的比喻，這些材料沒有建立政府對非拉丁文字另課稅的主張。MM原提案保留為「ai token tax for non-latin language」，不替換成已經證實、對所有模型一樣的成本倍數。原訊息 phonemsg-01M80VSZN5QG6J5SE2C7591KM1 未指定日期、順序或產品。

## 候選核心問題

「同樣的意思，換一種語言，為什麼可能花更多 AI 費用？」適合用一組經人工核對的平行文本，展示切分、模型改版及計價。非拉丁文字是MM指定的關注，不應把它改成只有中文與英文的對比；也不能把文字系統當成唯一原因。拉丁文字語言也可能有不同token負擔。

|層次|研究問題|應避免的推論|
|---|---|---|
|分詞|同一意思在指定tokenizer下需多少token？|字數或UTF-8位元組數不能直接當token數。|
|使用限制|固定token視窗可以放多少語意內容？|更多token不自動證明模型比較笨或品質較差。|
|計價|輸入、輸出、快取、推理token如何計費？|API的每token差異不等於聊天訂閱每句直接多收錢。|
|改善|不同詞彙表、切分方法及版本能否減少差異？|2023年的倍數不當成2026所有產品的現況。|

## 已核對的初步發現

Petrov等人的NeurIPS 2023作者研究頁說明，採FLORES-200平行語料的2000句比較17種tokenizer，部分語言配對可相差超過15倍。這是特定語料與當時tokenizer的研究結果，不是「所有非拉丁文字比英文貴15倍」。作者頁對ChatGPT/GPT-4採cl100k_base的標示也有其歷史版本，不能直接拿來指現在所有同品牌模型。

OpenAI目前token說明明確區分輸入、輸出、快取和推理token，也指出相同文字的token數會隨模型、encoding與語言改變。頁面指出推理token可能不出現在可見答案內、卻計入輸出；重新把畫面上的答案切分一次，不一定能還原帳單。這些是費用機制，尚未在本輪取得任何使用者帳單或執行付費API測試。

2024-05-13的GPT-4o公告列出20語言的指定示例與新版tokenizer壓縮結果，包括Gujarati145到33、Chinese34到24、Japanese37到26、English27到24。這些數字是廠商公布的示例，展示改版確實可以改變切分；不是本輪獨立量測、也不是相對英文的跨語言成本倍數，更不能把它們當2026通用結果。正式稿未必需要這些數字，可用來阻止把舊研究固定化。

2025年NeurIPS論文摘要研究約7000個可比較的單語tokenizer及97語言，指出詞彙表大小、pre-tokenization等選擇與token premium有關，並提出改善方案。COLING 2025摘要研究Tamil、Sinhala、Hindi的grapheme方法。兩者都支持「切分設計可以研究與改善」，目前只讀摘要，尚未核對完整方法、實驗表或效果大小，不能宣稱已完成全文評估。

獨立技術解說以cl100k_base及短語展示日文、英文和Hindi的切分，但其中Hindi用的是英文短語的轉寫而非真正同義翻譯。它可當切分示意線索，不宜成為跨語言公平性量測。文中UTF-8與code point的敘述也只能限其選定字例，不能推成Unicode通則。

另有2025年tokenization multiplicity論文指出相同可見輸出可能有不同token序列，提供「畫面一樣、使用量未必一樣」的補充方向。這不是主要語言差異機制，也不是本輪已獨立驗證的產品結論。

## 正式研究下一步

1. 選定少量具代表性的非拉丁文字語言，以及至少一種非英語拉丁文字語言作對照；人工核對平行語料的意思與文體。這仍是研究設計，不替MM決定只有中文版本。
2. 從完整2023與2025論文核對資料清洗、語言範圍、tokenizer名與版本。現階段3篇學術材料只有作者概述或摘要，沒有把摘要說成全文。
3. 若做原創圖，記錄可重現的開源encoding版本、文本與token序列。只做本地切分可以不花API費用；任何付費模型調用仍須另有金額授權。本輪沒有付費測試。
4. 發稿時再核模型與當日官方價表。按指定輸入/輸出情境算例，不把單一價格表或固定token倍數推成實際整體成本。
5. 圖像建議為原創平行文本切分圖與明確範圍的比較圖。尚未製圖、完成圖片評估或像素驗收，不採裝飾性機器人照片。

## 與近期選題的關係

核心是數位介面的計量與語言公平，不是032的語言技藝傳承，也不是036公共機構例外處理。仍要避免寫成只追問單位定義的另一篇數值解謎；把切分造成的使用選擇、可及性與設計取捨說清楚。兩個新提案都保留候選，尚未指定037或互相排序。

## 來源與閱讀範圍

1. Petrov等，NeurIPS 2023作者研究頁，作者公開資料與實驗說明，已讀頁面，未操作所有模型組合或完整讀PDF。
https://aleksandarpetrov.github.io/tokenization-fairness/
2. OpenAI，Understanding and counting tokens，讀取時顯示更新於16天前，官方技術/計費說明，已讀全文。支持分類、版本差異與應核實使用量，不提供此處任何固定價格。
https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens
3. OpenAI，Hello GPT-4o，2024-05-13，官方歷史發表，已讀Language tokenization表及前後文。只作指定示例與改版證據。
https://openai.com/index/hello-gpt-4o/
4. Arnett等，Explaining and Mitigating Crosslingual Tokenizer Inequities，NeurIPS 2025，學術摘要已讀，未核全文實驗。
https://proceedings.neurips.cc/paper_files/paper/2025/hash/5b91cefbfa52340af2f16f249572dc76-Abstract-Conference.html
5. Egalitarian Language Representation in Language Models: It All Begins with Tokenizers，COLING 2025，ACL學術摘要已讀，未核全文實驗。
https://aclanthology.org/2025.coling-main.400/
6. Leonie Monigatti，2023-08-16，獨立技術解說，已讀示例與方法。短句、轉寫和舊encoding僅作示意線索，不取其最高倍數為現在通則。
https://www.leoniemonigatti.com/blog/openai-cost-for-non-english.html
7. Tokenization Multiplicity Leads to Arbitrary Price Variation in LLM-as-a-service，2025-06-06起，研究預印本，已讀摘要與導論相關範圍，未完整評估方法。
https://arxiv.org/abs/2506.06446

本輪是候選簡報而非可發表全文，沒有現行全模型排行、語言稅金額、價格建議或未限定的倍數結論。
