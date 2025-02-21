# views/pages/meeting_detail.py
import streamlit as st
from services.meeting_service import MeetingService

class MeetingDetailView:
    def __init__(self):
        self.meeting_service = MeetingService()

    def render(self):
        if "selected_meeting_id" not in st.session_state:
            st.error("선택된 회의록이 없습니다.")
            return

        meeting = self.meeting_service.get_meeting(st.session_state.selected_meeting_id)
        if not meeting:
            st.error("회의록을 찾을 수 없습니다.")
            return

        st.title(f"회의록 상세 정보: {meeting.project_name}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**회의 일시**")
            st.write(meeting.meeting_date.strftime("%Y-%m-%d %H:%M"))
            st.write("**참석자**")
            st.write(", ".join(meeting.attendees))
            st.write("**장소**")
            st.write(meeting.location)
        with col2:
            st.write("**다음 회의 일시**")
            st.write(meeting.next_meeting_date.strftime("%Y-%m-%d %H:%M"))
            st.write("**다음 회의 장소**")
            st.write(meeting.next_meeting_location)

        st.write("**회의 내용**")
        st.write(meeting.meeting_content)
        
        st.write("**해야 할 일**")
        st.write(meeting.action_items)
        
        st.write("**특이사항**")
        st.write(meeting.special_notes)

        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            if st.button("목록으로"):
                st.session_state.current_page = "회의록 목록"
                st.rerun()
        with col2:
            if st.button("수정"):
                st.session_state.current_page = "회의록 수정"
                st.rerun()
        with col3:
            if st.button("삭제"):
                st.session_state.delete_confirm = True
                st.rerun()

        if "delete_confirm" in st.session_state and st.session_state.delete_confirm:
            st.warning("정말 삭제하시겠습니까?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("예", key="delete_yes"):
                    self.meeting_service.delete_meeting(meeting.id)
                    st.success("회의록이 삭제되었습니다.")
                    st.session_state.current_page = "회의록 목록"
                    st.rerun()
            with col2:
                if st.button("아니오", key="delete_no"):
                    st.session_state.delete_confirm = False
                    st.rerun()