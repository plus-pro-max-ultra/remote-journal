# gh直接編輯原始碼

文章與review全文的p／h2／figure等內容區塊各一行，保留段內a／sup等行內元素，不用prettify拆開中文字。發佈前先跑：

```sh
python scripts/format_article_source.py articles/0*/index.html review/*/index.html
python scripts/check_article_source.py
```

HTML是編輯權威。stories.js是JSON相容的資料鏡像，字串中的HTML保留escaped內容；不將body改成JavaScript拼接式以免破壞既有資料讀取。鏡像不可用來回填覆寫HTML。新增或重序列化文章、review後均重跑格式與檢查；以不計新增換行的原始位元組與DOM對比確認無文字改動。

2026-11-15修復：028與15篇review在新建／BeautifulSoup重序列化後漏跑既有formatter，造成整個reader-body壓成一行。另既有004／006／010／018的相鄰區塊一併分行。不改文字／屬性／來源／反思。
