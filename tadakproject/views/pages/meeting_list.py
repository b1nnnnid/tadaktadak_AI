# views/pages/meeting_list.py

import streamlit as st
from services.meeting_service import MeetingService

class MeetingListView:
    def __init__(self):
        self.meeting_service = MeetingService()

    def render(self):
        st.subheader("회의록 목록")

        if "search_type" not in st.session_state:
            st.session_state.search_type = "전체"
        if "search_keyword" not in st.session_state:
            st.session_state.search_keyword = ""

        col1, col2 = st.columns([2,1])
        with col1:
            st.session_state.search_type = st.selectbox(
                "검색 조건", 
                ["전체", "프로젝트명", "참석자"],
                index=["전체", "프로젝트명", "참석자"].index(st.session_state.search_type)
            )
        with col2:
            st.session_state.search_keyword = st.text_input("검색어")

        meetings = self.meeting_service.search_meetings(
            st.session_state.search_type,
            st.session_state.search_keyword
        )

        for meeting in meetings:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 4])
                with col1:
                    st.write(meeting.meeting_date.strftime("%Y-%m-%d %H:%M"))
                with col2:
                    st.write(meeting.project_name)
                with col3:
                    st.write(", ".join(meeting.attendees))
                with col4:
                    if st.button(f"{meeting.meeting_content[:50]}...", 
                               key=f"meeting_{meeting.id}"):
                        st.session_state.selected_meeting_id = meeting.id
                        st.session_state.current_page = "회의록 상세"
                        st.rerun()
                st.markdown("---")