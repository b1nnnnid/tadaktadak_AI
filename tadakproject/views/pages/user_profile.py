# views/pages/user_profile.py
import streamlit as st
from hashlib import sha256
from config.database import DatabaseConfig

class UserProfileView:
    # 회원정보 수정 페이지
    def __init__(self):
        self.conn = DatabaseConfig.get_connection()

    def render(self):
        if "username" not in st.session_state:
            st.warning("로그인이 필요합니다.")
            return

        st.title("내 정보")
        cursor = self.conn.cursor()
        st.markdown("---")
        # created_at이 없는 경우를 대비해 기본값 처리
        cursor.execute(
            "SELECT username, password, created_at FROM users WHERE username = ?", 
            (st.session_state.username,)
        )
        user = cursor.fetchone()

        if user:
            username, password, created_at = user
            st.write(f"**사용자 이름**: {username}")
            st.write(f"**비밀번호**: {'system_암호화됨'}")
            st.write(f"**회원가입 날짜**: {created_at}")
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("사용자 이름 수정"):
                    st.session_state.edit_mode = "username"
            with col2:
                if st.button("비밀번호 수정"):
                    st.session_state.edit_mode = "password"

            self._render_username_edit() if st.session_state.get('edit_mode') == "username" else None
            self._render_password_edit() if st.session_state.get('edit_mode') == "password" else None
        else:
            st.error("사용자 정보를 불러올 수 없습니다.")

    # [수정] 유저이름
    def _render_username_edit(self):
        password_check = st.text_input("현재 비밀번호", type="password", key="password_check_username")
        if password_check:
            if self._validate_password(password_check):
                new_username = st.text_input("새 사용자 이름", key="new_username",placeholder="수정을 취소할 경우 반드시 [취소]를 눌러주세요.")
                if st.button("저장하기"):
                    self._update_username(new_username)
            else:
                st.error("비밀번호가 일치하지 않습니다.")

        if st.button("취소"):
            st.session_state.edit_mode = None

    def _update_username(self, new_username: str):
            cursor = self.conn.cursor()
            
            # 중복 확인
            cursor.execute("SELECT * FROM users WHERE username = ?", (new_username,))
            if cursor.fetchone():
                st.error("이미 존재하는 사용자 이름입니다.")
                return

            try:
                cursor.execute(
                    "UPDATE users SET username = ? WHERE username = ?",
                    (new_username, st.session_state.username)
                )
                self.conn.commit()
                st.session_state.username = new_username  # 세션 업데이트
                st.success("사용자 이름이 수정되었습니다.")
                st.session_state.edit_mode = None
            except Exception as e:
                st.error(f"사용자 이름 수정 중 오류가 발생했습니다: {e}")

    # [수정] 비밀번호
    def _validate_password(self, password: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ?", 
            (st.session_state.username,)
        )
        stored_password = cursor.fetchone()[0]
        return sha256(password.encode()).hexdigest() == stored_password
    
    def _render_password_edit(self):
        password_check = st.text_input("현재 비밀번호", type="password", key="password_check_password",
                                     placeholder="현재 비밀번호 입력")
        
        if password_check:
            if self._validate_password(password_check):
                new_password = st.text_input("새 비밀번호", type="password", key="new_password",
                                           placeholder="유효하지 않은 데이터 입력 시 정상적인 로그인이 어려울 수 있습니다.")
                confirm_new_password = st.text_input("새 비밀번호 확인", type="password", 
                                                   key="confirm_new_password",
                                                   placeholder="수정을 취소할 경우 반드시 [취소]를 눌러주세요.")

                if st.button("저장하기"):
                    if new_password != confirm_new_password:
                        st.error("비밀번호가 일치하지 않습니다.")
                    else:
                        self._update_password(new_password)
            else:
                st.error("비밀번호가 일치하지 않습니다.")

        if st.button("취소"):
            st.session_state.edit_mode = None
                 
    def _update_password(self, new_password: str):
        cursor = self.conn.cursor()
        try:
            hashed_password = sha256(new_password.encode()).hexdigest()
            cursor.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (hashed_password, st.session_state.username)
            )
            self.conn.commit()
            st.success("비밀번호가 수정되었습니다.")
            st.session_state.edit_mode = None
        except Exception as e:
            st.error(f"비밀번호 수정 중 오류가 발생했습니다: {e}")

    def __del__(self):
        """데이터베이스 연결 정리"""
        if hasattr(self, 'conn'):
            self.conn.close()