# services/meeting_service.py

from typing import List, Optional
from datetime import datetime
from config.database import DatabaseConfig
from models.meeting import Meeting

class MeetingService:
    @classmethod
    def save_meeting(cls, meeting: Meeting) -> None:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO meeting_logs (
                project_name, attendees, meeting_date, location, meeting_content,
                action_items, next_meeting_date, next_meeting_location, special_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            meeting.project_name,
            ", ".join(meeting.attendees),
            meeting.meeting_date.isoformat(),
            meeting.location,
            meeting.meeting_content,
            meeting.action_items,
            meeting.next_meeting_date.isoformat(),
            meeting.next_meeting_location,
            meeting.special_notes
        ))
        conn.commit()
        conn.close()
    
    @classmethod
    def get_meeting(cls, meeting_id: int) -> Optional[Meeting]:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meeting_logs WHERE id = ?", (meeting_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return Meeting(
                id=result[0],
                project_name=result[1],
                attendees=result[2].split(", "),
                meeting_date=datetime.fromisoformat(result[3]),
                location=result[4],
                meeting_content=result[5],
                action_items=result[6],
                next_meeting_date=datetime.fromisoformat(result[7]),
                next_meeting_location=result[8],
                special_notes=result[9]
            )
        return None

    @classmethod
    def update_meeting(cls, meeting: Meeting) -> None:
        if not meeting.id:
            raise ValueError("Meeting ID is required for update")
            
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE meeting_logs 
            SET project_name = ?, attendees = ?, meeting_date = ?, location = ?,
                meeting_content = ?, action_items = ?, next_meeting_date = ?,
                next_meeting_location = ?, special_notes = ?
            WHERE id = ?
        """, (
            meeting.project_name,
            ", ".join(meeting.attendees),
            meeting.meeting_date.isoformat(),
            meeting.location,
            meeting.meeting_content,
            meeting.action_items,
            meeting.next_meeting_date.isoformat(),
            meeting.next_meeting_location,
            meeting.special_notes,
            meeting.id
        ))
        conn.commit()
        conn.close()

    @classmethod
    def delete_meeting(cls, meeting_id: int) -> None:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meeting_logs WHERE id = ?", (meeting_id,))
        conn.commit()
        conn.close()

    @classmethod
    def get_project_names(cls) -> List[str]:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT project_name FROM meeting_logs")
        projects = [row[0] for row in cursor.fetchall()]
        conn.close()
        return projects

    @classmethod
    def search_meetings(cls, search_type: str, keyword: str) -> List[Meeting]:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM meeting_logs"
        params = []
        
        if keyword:
            if search_type == "프로젝트명":
                query += " WHERE project_name LIKE ?"
                params.append(f"%{keyword}%")
            elif search_type == "참석자":
                query += " WHERE attendees LIKE ?"
                params.append(f"%{keyword}%")
            elif search_type == "전체":
                query += " WHERE project_name LIKE ? OR attendees LIKE ?"
                params.extend([f"%{keyword}%", f"%{keyword}%"])
                
        query += " ORDER BY meeting_date DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return [cls._row_to_meeting(row) for row in results]

    @classmethod
    def _row_to_meeting(cls, row) -> Meeting:
        return Meeting(
            id=row[0],
            project_name=row[1],
            attendees=row[2].split(", "),
            meeting_date=datetime.fromisoformat(row[3]),
            location=row[4],
            meeting_content=row[5],
            action_items=row[6],
            next_meeting_date=datetime.fromisoformat(row[7]),
            next_meeting_location=row[8],
            special_notes=row[9]
        )