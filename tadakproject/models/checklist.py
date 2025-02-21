# models/checklist.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChecklistItem:
    id: int
    item: str
    deadline: datetime
    added_on: datetime
    completed: bool = False