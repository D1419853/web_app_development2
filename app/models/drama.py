import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')

class Drama:
    def __init__(self, id=None, title=None, description=None, category=None, rating=0.0, image_url=None, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.rating = rating
        self.image_url = image_url
        self.created_at = created_at

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, title, description, category, rating, image_url):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO drama (title, description, category, rating, image_url) VALUES (?, ?, ?, ?, ?)',
            (title, description, category, rating, image_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @classmethod
    def get_all(cls):
        conn = cls.get_db_connection()
        rows = conn.execute('SELECT * FROM drama ORDER BY rating DESC').fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]

    @classmethod
    def get_by_id(cls, drama_id):
        conn = cls.get_db_connection()
        row = conn.execute('SELECT * FROM drama WHERE id = ?', (drama_id,)).fetchone()
        conn.close()
        if row:
            return cls(**dict(row))
        return None

    @classmethod
    def filter_by_category(cls, category):
        conn = cls.get_db_connection()
        rows = conn.execute('SELECT * FROM drama WHERE category LIKE ?', (f'%{category}%',)).fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]

    @classmethod
    def update(cls, drama_id, title, description, category, rating, image_url):
        conn = cls.get_db_connection()
        conn.execute(
            'UPDATE drama SET title = ?, description = ?, category = ?, rating = ?, image_url = ? WHERE id = ?',
            (title, description, category, rating, image_url, drama_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, drama_id):
        conn = cls.get_db_connection()
        conn.execute('DELETE FROM drama WHERE id = ?', (drama_id,))
        conn.commit()
        conn.close()
