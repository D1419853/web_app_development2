import sqlite3
import os

class Actor:
    def __init__(self, id=None, name=None, image_url=None):
        self.id = id
        self.name = name
        self.image_url = image_url

    @staticmethod
    def get_db_connection():
        """建立並回傳資料庫連線"""
        db_path = os.path.join('instance', 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, name, image_url):
        """新增一筆演員記錄"""
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO actor (name, image_url) VALUES (?, ?)',
                (name, image_url)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error creating actor: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有演員"""
        try:
            conn = cls.get_db_connection()
            rows = conn.execute('SELECT * FROM actor').fetchall()
            conn.close()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            print(f"Error getting actors: {e}")
            return []

    @classmethod
    def get_by_id(cls, actor_id):
        """根據 ID 取得單筆演員"""
        try:
            conn = cls.get_db_connection()
            row = conn.execute('SELECT * FROM actor WHERE id = ?', (actor_id,)).fetchone()
            conn.close()
            if row:
                return cls(**dict(row))
            return None
        except Exception as e:
            print(f"Error getting actor by id: {e}")
            return None

    @classmethod
    def update(cls, actor_id, name, image_url):
        """更新演員資訊"""
        try:
            conn = cls.get_db_connection()
            conn.execute(
                'UPDATE actor SET name = ?, image_url = ? WHERE id = ?',
                (name, image_url, actor_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating actor: {e}")
            return False

    @classmethod
    def delete(cls, actor_id):
        """刪除演員"""
        try:
            conn = cls.get_db_connection()
            conn.execute('DELETE FROM actor WHERE id = ?', (actor_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting actor: {e}")
            return False

    @classmethod
    def get_dramas_by_actor(cls, actor_id):
        """獲取該演員參與的所有劇集"""
        try:
            from app.models.drama import Drama
            conn = cls.get_db_connection()
            rows = conn.execute('''
                SELECT d.* FROM drama d
                JOIN drama_actor da ON d.id = da.drama_id
                WHERE da.actor_id = ?
            ''', (actor_id,)).fetchall()
            conn.close()
            return [Drama(**dict(row)) for row in rows]
        except Exception as e:
            print(f"Error getting dramas by actor: {e}")
            return []
