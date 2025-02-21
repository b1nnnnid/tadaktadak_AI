# views/pages/settings.py
import streamlit as st
import hashlib
from config.database import DatabaseConfig

class SettingsView:
    def __init__(self):
        self.conn = DatabaseConfig.get_connection()
        
    def render(self):
        st.title("회원 탈퇴")
        st.markdown("---")
        st.warning("회원 탈퇴 시 모든 정보가 삭제되며 복구할 수 없습니다.")
        st.write("계정을 삭제하시려면 비밀번호를 입력하세요.")
        
        password = st.text_input("비밀번호", type="password", key="password_delete")
        
        if st.button("탈퇴하기"):
            if not password:
                st.error("비밀번호를 입력하세요.")
                return
            
            try:
                cursor = self.conn.cursor()
                username = st.session_state.username
                
                # 현재 사용자 정보 가져오기
                cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                
                if not result:
                    st.error("사용자 정보가 없습니다. 다시 로그인하세요.")
                    return
                
                # 비밀번호 확인
                stored_password = result[0]
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                if stored_password != hashed_password:
                    st.error("비밀번호가 올바르지 않습니다.")
                else:
                    # 계정 삭제
                    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                    self.conn.commit()
                    
                    # 세션 초기화
                    del st.session_state.username
                    st.session_state.page = "login"
                    st.success("계정이 성공적으로 삭제되었습니다. 새로고침 시 초기 화면으로 이동합니다.")
                    st.rerun()
            
            except Exception as e:
                st.error(f"계정을 삭제하는 중 오류가 발생했습니다: {e}")
                
    def __del__(self):
        """데이터베이스 연결 정리"""
        if hasattr(self, 'conn'):
            self.conn.close()