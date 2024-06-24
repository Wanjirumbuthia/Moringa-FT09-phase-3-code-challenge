from database.connection import CURSOR, CONN

class Magazine:
    all_magazines = {}

    def __init__(self, id=None, name=None, category=None):
        self._id = id  
        self.name = name
        self.category = category
        if id is not None:    
            type(self).all_magazines[self.id] = self

    def __repr__(self):
        return f'<Magazine {self.name}, Category: {self.category}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self._id = value
        else:
            raise TypeError("id must be of type int")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be of type str")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be of type str")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value

    @classmethod
    def create_table(cls):
        """Create the magazines table if it doesn't exist."""
        sql = """CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );"""
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the magazines table."""
        sql = """
            DROP TABLE IF EXISTS magazines
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Save the magazine instance to the database."""
        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all_magazines[self.id] = self

    def update(self):
        """Update the magazine details in the database."""
        if hasattr(self, 'id'):
            sql = """
                UPDATE magazines
                SET name = ?, category = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.category, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, category):
        """Create a new magazine and save it to the database."""
        magazine = cls(name=name, category=category)
        magazine.save()
        return magazine

    def articles(self):
        """Retrieve articles associated with the magazine."""
        from models.article import Article
        sql = """
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            INNER JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        articles_data = CURSOR.fetchall()
        return [Article(*data) for data in articles_data]

    def contributors(self):
        """Retrieve authors who contributed to the magazine."""
        from models.author import Author
        sql = """
            SELECT authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
        """
        CURSOR.execute(sql, (self.id,))
        contributors_data = CURSOR.fetchall()
        return [Author(name=data[0]) for data in contributors_data]

    def article_titles(self):
        """Retrieve titles of articles in the magazine."""
        sql = """
            SELECT title
            FROM articles
            WHERE magazine_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        titles = CURSOR.fetchall()
        return [title[0] for title in titles]

    def contributing_authors(self):
        """Retrieve authors who contributed more than 2 articles to the magazine."""
        from models.author import Author
        sql = """
            SELECT authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(*) > 2
        """
        CURSOR.execute(sql, (self.id,))
        contributors_data = CURSOR.fetchall()
        return [Author(name=data[0]) for data in contributors_data]

    def delete(self):
        """Delete the magazine from the database."""
        sql = """
            DELETE FROM magazines
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all_magazines[self.id]