# views/pages/coworkers.py

import streamlit as st
from services.coworkers_services import CoworkersService
from services.ai_service import AIService

class CoworkersView:
    def __init__(self):
        self.personnel_service = CoworkersService
        self.ai_service = AIService()  # AI 서비스 추가됨 1203화 1658

    def render(self):
        st.title("인물 관리")
        
        personnel_list = self.personnel_service.get_all_coworkers()
        
        if personnel_list:
            selected_person = st.selectbox(
                "인물 선택",
                personnel_list,
                key="personnel_select"
            )
            # "인물 삭제" 버튼 추가
            if "delete_confirm" not in st.session_state:
                st.session_state.delete_confirm = False  # 삭제 확인 상태 초기화
            
            if st.button("인물 삭제"):
                st.session_state.delete_confirm = True  # 삭제 확인 플래그 설정
            
            if st.session_state.delete_confirm:
                st.warning(f"'{selected_person}'을(를) 정말 삭제하시겠습니까?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("확인"):
                        self.personnel_service.delete_person(selected_person)
                        st.success(f"'{selected_person}'이(가) 삭제되었습니다.")
                        st.session_state.delete_confirm = False  # 플래그 해제
                        st.rerun()  # 페이지 새로고침
                with col2:
                    if st.button("취소"):
                        st.session_state.delete_confirm = False  # 플래그 해제

            if selected_person:
                # 회의록 데이터 가져오기
                meeting_logs = self.personnel_service.get_all_meetings()
                # 분석 수행
                analysis_result = self.ai_service.analyze_person_mentions(
                    selected_person, meeting_logs
                )
                st.write(f"**AI 인물분석:**\n {analysis_result}")

            tab1, tab2 = st.tabs(["참석 회의록", "언급된 내용"])
            
            with tab1:
                self._render_attended_meetings(selected_person)
            
            with tab2:
                self._render_mentioned_content(selected_person)
        else:
            st.write("등록된 인물이 없습니다.")
            

    def _render_attended_meetings(self, selected_person: str):
        st.subheader(f"{selected_person}님이 참석한 회의록")
        
        meetings = self.personnel_service.get_attended_meetings(selected_person)
        if meetings:
            for meeting in meetings:
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 4])
                    with col1:
                        st.write(meeting[1])  # meeting_date
                    with col2:
                        st.write(meeting[2])  # project_name
                    with col3:
                        
                        content = meeting[3] if len(meeting) > 3 else "내용 없음"
                        if st.button(f"{content[:50]}...", 
                                key=f"meeting_{meeting[0]}"):
                            st.session_state.selected_meeting_id = meeting[0]
                            st.session_state.current_page = "회의록 상세"
                            st.rerun()
                    st.markdown("---")
        else:
            st.write("참석한 회의록이 없습니다.")


    def _render_mentioned_content(self, selected_person: str):
        st.subheader(f"{selected_person}님이 언급된 내용")
        
        mentions = self.personnel_service.get_mentioned_content(selected_person)

        # mentions 데이터가 빈 리스트인 경우 처리
        if not mentions:
            st.write("언급된 내용이 없습니다.")
            return

        for mention in mentions:
            with st.expander(f"{mention['meeting_date']} - {mention['project_name']}"):
                self._render_mention_details(mention, selected_person)


    def _render_mention_details(self, mention, selected_person: str):
        """언급된 내용의 세부사항을 표시합니다."""
        # 회의 내용
        if "meeting_content" in mention and selected_person in mention["meeting_content"]:
            st.write("**회의 내용:**")
            for para in mention["meeting_content"].split('\n'):
                if selected_person in para:
                    st.write(para)
            st.markdown("---")
        
        # 해야 할 일
        if "action_items" in mention and selected_person in mention["action_items"]:
            st.write("**해야 할 일:**")
            for task in mention["action_items"].split('\n'):
                if selected_person in task:
                    st.write(task)
            st.markdown("---")
        
        # 특이사항
        if "special_notes" in mention and selected_person in mention["special_notes"]:
            st.write("**특이사항:**")
            for note in mention["special_notes"].split('\n'):
                if selected_person in note:
                    st.write(note)

        if st.button("회의록 보기", key=f"view_meeting_{mention['id']}"):
            st.session_state.selected_meeting_id = mention["id"]
            st.session_state.current_page = "회의록 상세"
            st.rerun()