import sqlite3
import os

class Collection:
    def __init__(self, id=None, drama_id=None, added_at=None, drama_title=None, drama_image=None):
        self.id = id
        self.drama_id = drama_id
        self.added_at = added_at
        # 額外屬性，用於顯示詳情
        self.drama_title = drama_title
        self.drama_image = drama_image

    @staticmethod
    def get_db_connection():
        """建立並回傳資料庫連線"""
        db_path = os.path.join('instance', 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def add(cls, drama_id):
        """將劇集加入收藏"""
        try:
            conn = cls.get_db_connection()
            # 檢查是否已存在，避免重複加入
            existing = conn.execute('SELECT id FROM collection WHERE drama_id = ?', (drama_id,)).fetchone()
            if not existing:
                conn.execute('INSERT INTO collection (drama_id) VALUES (?)', (drama_id,))
                conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding to collection: {e}")
            return False

    @classmethod
    def get_all(cls):
        """獲取所有收藏的劇集，包含劇集詳細資訊"""
        try:
            conn = cls.get_db_connection()
            rows = conn.execute('''
                SELECT c.*, d.title as drama_title, d.image_url as drama_image 
                FROM collection c
                JOIN drama d ON c.drama_id = d.id
                ORDER BY c.added_at DESC
            ''').fetchall()
            conn.close()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            print(f"Error getting collection: {e}")
            return []

    @classmethod
    def remove(cls, drama_id):
        """從收藏中移除指定劇集"""
        try:
            conn = cls.get_db_connection()
            conn.execute('DELETE FROM collection WHERE drama_id = ?', (drama_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error removing from collection: {e}")
            return False
            
    @classmethod
    def is_collected(cls, drama_id):
        """檢查某部劇是否已被收藏"""
        try:
            conn = cls.get_db_connection()
            row = conn.execute('SELECT id FROM collection WHERE drama_id = ?', (drama_id,)).fetchone()
            conn.close()
            return row is not None
        except Exception as e:
            print(f"Error checking collection status: {e}")
            return False
