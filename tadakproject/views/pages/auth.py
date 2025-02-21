# views/pages/auth.py
import streamlit as st
import time
import hashlib
from services.auth_service import AuthService

class AuthView:
    def __init__(self):
        self.auth_service = AuthService()

    def render_login(self):
        st.title("타닥타닥-AI 업무일지⌨️")
        
        username = st.text_input("사용자 이름", key="username_login")
        password = st.text_input("비밀번호", type="password", key="password_login")
        
        if st.button("로그인"):
            user = self.auth_service.get_user(username)  # get_user 메서드 추가 필요
            if user:
                # User 모델의 hash_password 메서드 사용
                from models.user import User
                hashed_password = User.hash_password(password)
                if hashed_password == user[2]:
                    st.success(f"{username}님, 환영합니다!")
                    time.sleep(2)
                    st.session_state["username"] = username
                    st.session_state.page = "main"
                    st.session_state.current_page = "main"
                    st.rerun()
                else:
                    st.error("비밀번호가 잘못되었습니다.")
            else:
                st.error("존재하지 않는 사용자명입니다.")

        if st.button("아직 계정이 없으신가요?"):
            st.session_state.page = "register"  # 회원가입 화면으로 이동
            st.session_state.current_page = "register"  # 회원가입 화면으로 이동
            st.rerun()  # 페이지 새로고침

    def render_register(self):
        st.title("회원가입")
        
        username = st.text_input("사용자 이름", key="username_register")
        password = st.text_input("비밀번호", type="password", key="password_register")
        confirm_password = st.text_input(
            "비밀번호 확인", 
            type="password", 
            key="confirm_password_register"
        )
        
        if st.button("가입하기"):
            if password != confirm_password:
                st.error("비밀번호가 일치하지 않습니다.")
            elif self.auth_service.register(username, password):
                st.success("타닥타닥에 오신 걸 환영합니다!")
                st.write("새로고침 후 로그인을 진행해주세요.")
            else:
                st.error