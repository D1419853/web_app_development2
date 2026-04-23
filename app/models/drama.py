import sqlite3
import os
from flask import current_app

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
        """建立並回傳資料庫連線"""
        db_path = os.path.join('instance', 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, title, description, category, rating, image_url):
        """
        新增一筆劇集記錄
        :param title: 劇集名稱
        :param description: 描述
        :param category: 類型
        :param rating: 評分
        :param image_url: 海報連結
        :return: 新紀錄的 ID
        """
        try:
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
        except Exception as e:
            print(f"Error creating drama: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有劇集，預設依評分降序排列
        :return: Drama 物件列表
        """
        try:
            conn = cls.get_db_connection()
            rows = conn.execute('SELECT * FROM drama ORDER BY rating DESC').fetchall()
            conn.close()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            print(f"Error getting dramas: {e}")
            return []

    @classmethod
    def get_by_id(cls, drama_id):
        """
        根據 ID 取得單筆劇集
        :param drama_id: 劇集 ID
        :return: Drama 物件或 None
        """
        try:
            conn = cls.get_db_connection()
            row = conn.execute('SELECT * FROM drama WHERE id = ?', (drama_id,)).fetchone()
            conn.close()
            if row:
                return cls(**dict(row))
            return None
        except Exception as e:
            print(f"Error getting drama by id: {e}")
            return None

    @classmethod
    def update(cls, drama_id, title, description, category, rating, image_url):
        """
        更新指定 ID 的劇集內容
        """
        try:
            conn = cls.get_db_connection()
            conn.execute(
                'UPDATE drama SET title = ?, description = ?, category = ?, rating = ?, image_url = ? WHERE id = ?',
                (title, description, category, rating, image_url, drama_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating drama: {e}")
            return False

    @classmethod
    def delete(cls, drama_id):
        """
        刪除指定 ID 的劇集
        """
        try:
            conn = cls.get_db_connection()
            conn.execute('DELETE FROM drama WHERE id = ?', (drama_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting drama: {e}")
            return False

    @classmethod
    def search(cls, query):
        """
        根據關鍵字搜尋標題或描述
        """
        try:
            conn = cls.get_db_connection()
            search_query = f'%{query}%'
            rows = conn.execute(
                'SELECT * FROM drama WHERE title LIKE ? OR description LIKE ?',
                (search_query, search_query)
            ).fetchall()
            conn.close()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            print(f"Error searching drama: {e}")
            return []
