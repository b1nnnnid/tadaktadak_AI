# make_db.py

import os
from config.database import DatabaseConfig

def delete_database():
    """기존 데이터베이스 파일이 있다면 삭제합니다."""
    db_path = DatabaseConfig.get_database_path()
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"{db_path} 파일이 삭제되었습니다.")
    else:
        print(f"{db_path} 파일이 존재하지 않습니다.")

def initialize():
    """데이터베이스를 초기화합니다."""
    print("데이터베이스 초기화를 시작합니다...")
    delete_database()  # 기존 DB 삭제
    DatabaseConfig.initialize_database()  # 새로운 DB 생성 및 초기화
    print("데이터베이스 초기화가 완료되었습니다.")

if __name__ == "__main__":
    initialize()