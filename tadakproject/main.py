# main.py

import streamlit as st
from views.components import load_global_styles
from dotenv import load_dotenv
from config.database import DatabaseConfig
from views.pages.auth import AuthView
from views.pages.main_page import MainPageView
from views.pages.meeting_form import MeetingFormView
from views.pages.meeting_list import MeetingListView
from views.pages.meeting_detail import MeetingDetailView
from views.pages.coworkers import CoworkersView
from views.pages.settings import SettingsView
from views.pages.user_profile import UserProfileView
from apscheduler.schedulers.background import BackgroundScheduler
from services.ai_service import AIService

# APScheduler 설정
scheduler = BackgroundScheduler()
ai_service = AIService()

# AI 분석 작업 (1시간마다 실행)
scheduler.add_job(ai_service.generate_main_analysis, 'interval', hours=1)
scheduler.add_job(ai_service.generate_recommendations, 'interval', hours=1)

# 스케줄러 시작
scheduler.start()


# 메인 페이지 설정
st.set_page_config(page_title="타닥타닥 ⌨️", page_icon="⌨️🔥", layout="wide")

# 공통 스타일: 글꼴 적용
load_global_styles()

# 환경 변수 로드
load_dotenv()


def initialize_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"

def render_sidebar():
    username = st.session_state.username
    st.sidebar.title("타닥타닥-AI 업무일지⌨️")
    st.sidebar.markdown(
        f"<p style='font-size: 16px; font-weight: bold; margin-bottom: 20px;'>{username}님, 오늘도 화이팅입니다!</p>",
        unsafe_allow_html=True
        )
    
    menu_options = ["메인페이지", "회의록 작성", "회의록 목록", "인물관리"]
    setting_options = ["내 정보", "환경설정"]
    
    st.sidebar.markdown("### 메뉴")
    for option in menu_options:
        if st.sidebar.button(option, key=f"menu_{option}"):
            st.session_state.current_page = option
            st.rerun()
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 설정")
    for option in setting_options:
        if st.sidebar.button(option, key=f"setting_{option}"):
            st.session_state.current_page = option
            st.rerun()

def render_current_page():
    page_views = {
        "메인페이지": MainPageView,
        "회의록 작성": MeetingFormView,
        "회의록 목록": MeetingListView,
        "회의록 상세": MeetingDetailView,
        "회의록 수정": MeetingDetailView,  # 수정 페이지도 MeetingDetailView에서 처리
        "인물관리": CoworkersView,
        "환경설정": SettingsView,
        "내 정보": UserProfileView
    }
    
    current_page = st.session_state.current_page
    view_class = page_views.get(current_page, MainPageView)
    view = view_class()

    if current_page == "회의록 수정":
        view.render_edit()
    else:
        view.render()

def main():
    # 메인 애플리케이션 실행
    initialize_session_state()
    
    # 로그인 상태에 따른 페이지 렌더링
    if st.session_state.page == "login":
        auth_view = AuthView()
        auth_view.render_login()
    elif st.session_state.page == "register":
        auth_view = AuthView()
        auth_view.render_register()
    elif st.session_state.page == "main":        
        render_sidebar()
        render_current_page()


# Streamlit 종료 시 스케줄러 종료
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        