# views/pages/meeting_form.py

import streamlit as st
from datetime import datetime
from services.meeting_service import MeetingService
from services.coworkers_services import CoworkersService
from models.meeting import Meeting

class MeetingFormView:
    def __init__(self):
        self.meeting_service = MeetingService()
        self.personnel_service = CoworkersService()

    def render(self):
        st.subheader("회의록 작성")
        
        project_name = st.text_input("프로젝트명 입력 (자동완성 지원)")
        if project_name:
            existing_projects = self.meeting_service.get_project_names()
            filtered_projects = [p for p in existing_projects 
                               if project_name.lower() in p.lower()]
            if filtered_projects:
                st.write("자동완성 결과:")
                for proj in filtered_projects:
                    st.write(f"- {proj}")

        participants = self.personnel_service.get_all_coworkers()
        new_participant = st.text_input(
            "새로운 인물 추가", 
            placeholder="인물 이름을 입력하세요."
        )
        if st.button("인물 추가") and new_participant:
            if new_participant not in participants:
                self.personnel_service.add_person(new_participant)
                st.success(f"'{new_participant}'이(가) 추가되었습니다!")
                st.rerun()
            else:
                st.warning("이미 등록된 인물입니다.")

        selected_participants = st.multiselect(
            "참석자 선택",
            participants,
            placeholder="참석자를 선택하세요."
        )

        meeting_date = st.date_input("회의 날짜")
        meeting_time = st.text_input("회의 시간:", placeholder="예시) 14:00")
        location = st.text_input("장소")
        meeting_content = st.text_area("회의 내용")
        action_items = st.text_area("해야 할 일")

        next_meeting_date = st.date_input("다음 회의 날짜")
        next_meeting_time = st.text_input("다음 회의 시간:", placeholder="예시) 14:00")
        next_meeting_location = st.text_input("다음 회의 장소")
        special_notes = st.text_area("특이사항")

        if st.button("저장"):
            if project_name and selected_participants and location:
                meeting = Meeting(
                    project_name=project_name,
                    attendees=selected_participants,
                    meeting_date=datetime.combine(
                        meeting_date, 
                        datetime.strptime(meeting_time, "%H:%M").time()
                    ),
                    location=location,
                    meeting_content=meeting_content,
                    action_items=action_items,
                    next_meeting_date=datetime.combine(
                        next_meeting_date,
                        datetime.strptime(next_meeting_time, "%H:%M").time()
                    ),
                    next_meeting_location=next_meeting_location,
                    special_notes=special_notes
                )
                self.meeting_service.save_meeting(meeting)
                st.success("회의록이 저장되었습니다!")
                st.session_state.current_page = "회의록 목록"
                st.rerun()
            else:
                st.warning("프로젝트명, 참석자, 장소는 필수 입력 항목입니다.")