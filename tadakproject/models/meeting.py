# models/meeting.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Meeting:
    project_name: str
    attendees: List[str]
    meeting_date: datetime
    location: str
    meeting_content: str
    action_items: str
    next_meeting_date: datetime
    next_meeting_location: str
    special_notes: str
    id: Optional[int] = None