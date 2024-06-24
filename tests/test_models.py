import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):

    def test_author_creation(self):
        author = Author(name="John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(title="Test Title", content="Test Content", author_id=1, magazine_id=1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_author_name_change(self):
        author = Author(name="John Doe")
        with self.assertRaises(AttributeError):
            setattr(author, 'name', "Jane Doe")

    def test_author_name_length(self):
        with self.assertRaises(ValueError):
            author = Author(name="")

    def test_author_name_type(self):
        with self.assertRaises(TypeError):
            author = Author(123)

    def test_article_title_length(self):
        with self.assertRaises(ValueError):
            article = Article(title="", content="Test Content", author_id=1, magazine_id=1)

    def test_magazine_name_type(self):
        with self.assertRaises(TypeError):
            magazine = Magazine(name=123, category="Technology")

    def test_magazine_name_length(self):
        with self.assertRaises(ValueError):
            magazine = Magazine(name="", category="Technology")

    def test_author_articles(self):
        author = Author(name="John Doe")
        articles = author.articles()
        self.assertEqual(len(articles), 0)

    def test_author_magazines(self):
        author = Author(name="John Doe")
        magazines = author.magazines()
        self.assertEqual(len(magazines), 0)

    def test_magazine_articles(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        articles = magazine.articles()
        self.assertEqual(len(articles), 0)

    def test_magazine_contributors(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        contributors = magazine.contributors()
        self.assertEqual(len(contributors), 0)

    def test_magazine_article_titles(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        titles = magazine.article_titles()
        self.assertEqual(len(titles), 0)

    def test_magazine_contributing_authors(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        contributing_authors = magazine.contributing_authors()
        self.assertEqual(len(contributing_authors), 0)

if __name__ == "__main__":
    unittest.main()