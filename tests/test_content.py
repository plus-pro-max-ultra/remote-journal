import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = ROOT / "content" / "articles"
DRAFT_DIR = ROOT / "drafts"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class ContentQualityTests(unittest.TestCase):
    def test_published_article_ids_are_unique(self):
        articles = [read_json(path) for path in ARTICLE_DIR.glob("*.json")]
        ids = [article.get("id") for article in articles]
        self.assertTrue(articles, "至少需要一篇正式文章")
        self.assertEqual(len(ids), len(set(ids)), "正式文章的 id 不可重複")
        for article_id in ids:
            self.assertRegex(article_id or "", r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_published_articles_have_core_fields_and_sources(self):
        for path in ARTICLE_DIR.glob("*.json"):
            with self.subTest(file=path.name):
                story = read_json(path)
                for key in ("title", "subtitle", "category", "tags", "minutes", "intro", "reflection", "sources"):
                    self.assertIn(key, story)
                    self.assertTrue(story[key] or key == "tags", f"{path.name}: {key} 不應為空")
                self.assertTrue(story.get("body") or story.get("sections"), f"{path.name}: 沒有正文")
                self.assertGreaterEqual(len(story["sources"]), 2)
                for source in story["sources"]:
                    url = source[1] if isinstance(source, list) else source.get("url", "")
                    self.assertTrue(url.startswith("https://"), f"{path.name}: 非 HTTPS 來源 {url}")

    def test_structured_sections_are_renderable(self):
        for path in list(ARTICLE_DIR.glob("*.json")) + list(DRAFT_DIR.glob("*.json")):
            with self.subTest(file=path.name):
                story = read_json(path)
                if "sections" not in story:
                    continue
                self.assertGreaterEqual(len(story["sections"]), 4)
                for section in story["sections"]:
                    self.assertTrue(section.get("heading"))
                    self.assertGreaterEqual(len(section.get("paragraphs", [])), 2)

    def test_daily_draft_schema_if_present(self):
        for path in DRAFT_DIR.glob("*.json"):
            with self.subTest(file=path.name):
                story = read_json(path)
                for key in ("id", "title", "subtitle", "category", "tags", "minutes", "intro", "sections", "reflection", "sources", "related"):
                    self.assertIn(key, story)
                self.assertGreaterEqual(len(story["sources"]), 3)
                for source in story["sources"]:
                    self.assertTrue(source.get("url", "").startswith("https://"))

if __name__ == "__main__":
    unittest.main()
