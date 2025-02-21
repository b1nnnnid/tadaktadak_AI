# services/coworkers_service.py

from typing import List, Tuple, Dict
from config.database import DatabaseConfig

class CoworkersService:
    @classmethod
    def get_all_coworkers(cls) -> List[str]:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM coworkers")
        personnel = [row[0] for row in cursor.fetchall()]
        conn.close()
        return personnel
    
    @classmethod
    def add_person(cls, name: str) -> None:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO coworkers (name, info) VALUES (?, ?)", 
            (name, "")
        )
        conn.commit()
        conn.close()
        
    @classmethod
    def delete_person(cls, name: str) -> None:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM coworkers WHERE name = ?", 
            (name,)
        )
        conn.commit()
        conn.close()

    @classmethod
    def get_attended_meetings(cls, person: str) -> List[Tuple]:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, meeting_date, project_name, meeting_content
            FROM meeting_logs
            WHERE attendees LIKE ?
            ORDER BY meeting_date DESC
        """, (f"%{person}%",))
        meetings = cursor.fetchall()
        conn.close()
        return meetings

    @classmethod
    def get_mentioned_content(cls, person: str) -> List[Dict]:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, meeting_date, project_name, meeting_content, action_items, special_notes
            FROM meeting_logs
            WHERE 
                meeting_content LIKE ? OR
                action_items LIKE ? OR
                special_notes LIKE ?
            ORDER BY meeting_date DESC
        """, (f"%{person}%", f"%{person}%", f"%{person}%"))
        mentions = cursor.fetchall()
        conn.close()

        # 데이터를 딕셔너리로 변환하여 반환
        return [
            {
                "id": row[0],
                "meeting_date": row[1],
                "project_name": row[2],
                "meeting_content": row[3],
                "action_items": row[4],
                "special_notes": row[5],
            }
            for row in mentions
        ]

    @classmethod
    def get_all_meetings(cls) -> List[Dict]:
        """
        모든 회의록 데이터를 가져옵니다.
        :return: 회의록 데이터 리스트
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, project_name, meeting_date, meeting_content
            FROM meeting_logs
        """)
        rows = cursor.fetchall()
        conn.close()
        
        # 데이터를 딕셔너리 형태로 변환
        meeting_logs = [
            {
                "id": row[0],
                "project_name": row[1],
                "meeting_date": row[2],
                "meeting_content": row[3],
            }
            for row in rows
        ]
        return meeting_logs