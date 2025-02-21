# services/checklist_service.py

from datetime import datetime
from config.database import DatabaseConfig
from typing import List
from models.checklist import ChecklistItem

class ChecklistService:
    @staticmethod
    def init_db():
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                deadline TEXT NOT NULL,
                added_on TEXT NOT NULL,
                completed BOOLEAN NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def add_item(item: str, deadline: datetime, added_on: datetime) -> None:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO checklist (item, deadline, added_on, completed)
            VALUES (?, ?, ?, ?)
        ''', (item, deadline.strftime('%Y-%m-%d'), 
              added_on.strftime('%Y-%m-%d %H:%M:%S'), False))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_items() -> List[ChecklistItem]:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM checklist ORDER BY completed, deadline, added_on')
        rows = cursor.fetchall()
        conn.close()
        
        return [ChecklistItem(
            id=row[0],
            item=row[1],
            deadline=datetime.strptime(row[2], '%Y-%m-%d'),
            added_on=datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
            completed=bool(row[4])
        ) for row in rows]

    @staticmethod
    def delete_item(item_id: int) -> None:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM checklist WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_item(item_id: int, completed: bool) -> None:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE checklist SET completed = ? WHERE id = ?', 
                      (completed, item_id))
        conn.commit()
        conn.close()