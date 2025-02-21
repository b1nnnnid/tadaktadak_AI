# config/database.py

import os
import sqlite3
from hashlib import sha256
from datetime import datetime

class DatabaseConfig:
    # 데이터 베이스 파일명 정의
    DB_NAME = "tadaktadak_database.db"
    
    @classmethod
    # 데이터 베이스 파일의 절대 경로 반환
    def get_database_path(cls):
        return os.path.abspath(cls.DB_NAME)
    
    @classmethod
    # SQLite 데이터 연결을 생성하고 반환
    def get_connection(cls):
        return sqlite3.connect(cls.DB_NAME)  # 데이터베이스 연결 객체
    
    @classmethod
    # 데이터베이스 초기화 및 필요한 테이블 생성
    def initialize_database(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()
        # 테이블 생성: meeting_logs (회의록 정보 저장)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meeting_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                attendees TEXT,
                meeting_date TEXT,
                location TEXT,
                meeting_content TEXT,
                action_items TEXT,
                next_meeting_date TEXT,
                next_meeting_location TEXT,
                special_notes TEXT
            )
        """)
        
        # 테이블 생성: coworkers (회의록 정보 저장)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coworkers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                info TEXT
            )
        """)
        
        # 체크리스트 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                deadline TEXT NOT NULL,
                added_on TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        
        
        # 테이블 생성: users (사용자 정보 저장: 회원가입, 로그인, 회원탈퇴 등)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # config/database.py의 initialize_database 메서드에 추가
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,  -- 생성 시간
                type TEXT,                                  -- 유형
                content TEXT,                               -- 내용
                source_type TEXT,                           -- 출처 유형
                source_id INTEGER,                          -- 원본 데이터 ID
                source_created_at TEXT                      -- 원본 데이터 생성일자
            )
        """)

        # main page의 AI 분석 결과 데이터를 1시간마다 생성하고 저장하는 데이터베이스
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS main_ai_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,                  -- 'main_suggestions' 또는 'recommendations'
                content TEXT,               -- 분석 결과
                created_at TEXT DEFAULT CURRENT_TIMESTAMP -- 생성 시간
            )
        """)

        # 테스트용 기본 사용자 계정 생성
        # 비밀번호는 SHA256으로 해시되어 저장됨
        # 기존에 없는 경우에만 기본 사용자 추가 (IGNORE 사용)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        default_users = [
            ("aaa", sha256("aaaaa123".encode()).hexdigest(), current_time),
            ("sss", sha256("sssss123".encode()).hexdigest(), current_time),
        ]
        
        for username, password, created_at in default_users:
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password, created_at) VALUES (?, ?, ?)",
                (username, password, created_at)
            )

        # 변경사항 저장 및 연결 종료        
        conn.commit()
        conn.close()
        print(f"{cls.DB_NAME} 데이터베이스가 초기화되었습니다.")