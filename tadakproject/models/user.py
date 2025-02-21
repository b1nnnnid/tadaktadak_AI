# models/user.py
from dataclasses import dataclass
from hashlib import sha256

@dataclass
class User:
    username: str
    password: str
    id: int = None
    
    @staticmethod
    def hash_password(password: str) -> str:
        return sha256(password.encode()).hexdigest()