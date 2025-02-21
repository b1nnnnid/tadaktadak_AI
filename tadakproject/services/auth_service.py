# services/auth_service.py

from config.database import DatabaseConfig
from hashlib import sha256
from typing import Optional, Tuple
from models.user import User

class AuthService:
    @classmethod
    def get_user(cls, username: str) -> Optional[Tuple]:
        # 사용자 정보 조회
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def login(cls, username: str, password: str) -> bool:
        # 사용자 로그인 처리
        user = cls.get_user(username)  # get_user 코드 재사용 
        if user:
            return User.hash_password(password) == user[2]
        return False
    
    @staticmethod
    def register(username: str, password: str) -> bool:
        # 새로운 사용자 등록
        if AuthService.get_user(username):  # get_user 메서드 재사용
            return False         
           
        hashed_password = User.hash_password(password)
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        conn.close()
        return True