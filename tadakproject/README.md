# README.md
# 타닥타닥-AI 업무일지

## 설치 방법
1. 가상환경 생성 및 활성화
```bash
python -m streamlit_env venv
source streamlit_env/bin/activate  # Windows: streamlit_env\Scripts\activate
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. 데이터베이스 초기화
```bash
python make_db.py
```

4. 애플리케이션 실행
```bash
streamlit run main.py
```

## 프로젝트 구조
```
project/
├── main.py                  # 메인 실행 파일
├── make_db.py              # 데이터베이스 설정 및 초기화 실행 파일
├── requirements.txt        # 필요한 패키지 목록
├── config/
│   └── database.py         # 데이터베이스 설정 및 초기화 로직
├── models/                 # 데이터 모델
│   ├── user.py
│   ├── meeting.py
│   └── checklist.py
├── services/              # 비즈니스 로직
│   ├── auth_service.py
│   ├── meeting_service.py
│   └── coworkers_sercive.py
└── views/                 # UI 컴포넌트
    ├── components/
    │   └── checklist.py
    └── pages/
        ├── auth.py
        ├── coworkers.py
        ├── main_page.py
        ├── meeting_form.py
        ├── meeting_list.py
        └── meeting_detail.py
```

## 기본 계정
- 사용자명: aaa / 비밀번호: aaaaa123
- 사용자명: sss / 비밀번호: sssss123

## 주요 기능
1. 회의록 관리
   - 회의록 작성
   - 회의록 조회/수정/삭제
   - 프로젝트별, 참석자별 검색

2. 인물 관리
   - 참석자 등록/관리
   - 인물별 참석 회의록 조회
   - 인물 언급 내용 검색

3. 체크리스트
   - 할 일 등록/관리
   - 마감일 설정
   - 완료 상태 관리