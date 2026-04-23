import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')

class Collection:
    def __init__(self, id=None, drama_id=None, added_at=None, drama_title=None):
        self.id = id
        self.drama_id = drama_id
        self.added_at = added_at
        # 額外屬性，用於顯示標題
        self.drama_title = drama_title

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def add(cls, drama_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        # 檢查是否已收藏，避免重複
        existing = conn.execute('SELECT id FROM collection WHERE drama_id = ?', (drama_id,)).fetchone()
        if not existing:
            cursor.execute('INSERT INTO collection (drama_id) VALUES (?)', (drama_id,))
            conn.commit()
        conn.close()

    @classmethod
    def get_all(cls):
        """獲取所有收藏的劇集，包含劇集詳細資訊"""
        conn = cls.get_db_connection()
        rows = conn.execute('''
            SELECT c.*, d.title as drama_title FROM collection c
            JOIN drama d ON c.drama_id = d.id
            ORDER BY c.added_at DESC
        ''').fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]

    @classmethod
    def remove(cls, drama_id):
        conn = cls.get_db_connection()
        conn.execute('DELETE FROM collection WHERE drama_id = ?', (drama_id,))
        conn.commit()
        conn.close()
