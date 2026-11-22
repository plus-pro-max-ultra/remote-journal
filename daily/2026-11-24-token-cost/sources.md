#037來源與採用範圍

1. Language Model Tokenizers Introduce Unfairness Between Languages，Petrov等，NeurIPS 2023
https://proceedings.nips.cc/paper_files/paper/2023/file/74bb24dca8334adce292883b4b651eda-Paper-Conference.pdf
第三、四節：FLORES-200平行語料、版本與語言差異，以及費用與context。已讀PDFpp1–8相關方法結果與限制討論；不將舊模型視窗或舊價格當現況。

2. Understanding and counting tokens，OpenAI
https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens
第一、四節：token定義、依encoding計數、輸入／輸出／快取／推理分類；費率依類別不同，文字重切不等於整請求用量。2026-11-22核讀，未引用固定單價。

3. tiktoken，OpenAI，MIT License
https://github.com/openai/tiktoken
第一節與原創示例：tiktoken0.14.0實際本地測得cl100k_base/o200k_base純文字數，無付費API呼叫；原始文字、ID與方法另存。

4. Egalitarian Language Representation in Language Models: It All Begins with Tokenizers，Velayuthan與Sarveswaran，COLING 2025
https://aclanthology.org/2025.coling-main.400/
第二節：實讀PDFpp5987–5992相關背景、方法與前置切分；Tamil/Sinhala/Hindi的字素組合與切分邊界。不把pre-token分析當完整模型品質測試。

5. Hello GPT-4o，OpenAI，2024-05-13
https://openai.com/index/hello-gpt-4o/
第三節：官方歷史公告二十語言指定示例，展示新tokenizer壓縮改善；不採為2026所有模型基準或跨語言固定價差。

6. Explaining and Mitigating Crosslingual Tokenizer Inequities，Arnett等，NeurIPS 2025
https://proceedings.neurips.cc/paper_files/paper/2025/file/5b91cefbfa52340af2f16f249572dc76-Paper-Conference.pdf
第五節：實讀pp1–10含方法、介入、討論與限制。約7000單語tokenizer97語言、語言詞彙表與跨空格合併；未訓練完整LM，FLORES翻譯品質限制。不稱品質已改善。

7. AI models cost more when you don’t use English，Ananya Bhattacharya，Rest of World，2026-10-26
https://restofworld.org/2026/ai-tokenizer-tax-non-english-languages-cost-inequity/
第四、六節：獨立新聞報導的教學context例與公開同任務表現／費用的討論。未直接核讀其CLEAR新研究，故不取報導中17倍或200語言等新數值作本文證據。
