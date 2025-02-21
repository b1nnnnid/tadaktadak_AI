import streamlit as st
from datetime import datetime
from services.checklist_service import ChecklistService

class ChecklistComponent:
    def __init__(self):
        self.service = ChecklistService()
        # 데이터베이스 초기화
        self.service.init_db()
        # 세션 상태 초기화
        if 'checklist' not in st.session_state:
            st.session_state['checklist'] = self.service.get_all_items()

    def render(self):
        # 스타일 정의
        st.markdown("""
            <style>
            .completed { color: grey; text-decoration: line-through; }
            .checklist-item { display: flex; align-items: center; margin-bottom: 10px; }
            .checklist-item span { margin-left: 10px; }
            
                        /* 폼 컨테이너 크기 설정 */
            div[data-testid="stForm"] {
                width: 110%;
                margin: 0 auto;
                margin-left: -2.8%;  /* 왼쪽으로 10%만큼 이동 */
                padding: 20px;
            }

            div[data-testid="stHorizontalBlock"] div.stButton > button {
                width: 75px; /* 버튼 너비 */
                height: 20px; /* 버튼 높이 * /
                cursor: pointer; /* 클릭 가능한 상태 */
            }
            div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            }
                    
            div[data-testid="stForm"] button.stButton {
                margin-top: 70px;  /* 버튼 위쪽에 20px 간격 추가 */
                display: flex;
                justify-content: center;  /* 버튼을 가운데 정렬 */
            }        
            </style>
        """, unsafe_allow_html=True)

        st.subheader("TO-DO✔️")
        
        # 입력 폼
        with st.form(key="checklist_form"):
            col1_1, col1_2, col1_3 = st.columns([3, 2, 1])
            with col1_1:
                new_item = st.text_input("새 항목", placeholder="할 일을 입력하세요")
            with col1_2:
                deadline = st.date_input("마감기한", value=datetime.now().date())
            with col1_3:
                submit_button = st.form_submit_button(label="✅")

            if submit_button and new_item:
                # 중복 체크
                checklist = st.session_state['checklist']
                if any(item.item == new_item and item.deadline.date() == deadline 
                      for item in checklist):
                    st.warning("이미 동일한 항목과 마감기한이 존재합니다.")
                else:
                    added_on = datetime.now()
                    self.service.add_item(new_item, deadline, added_on)
                    st.session_state['checklist'] = self.service.get_all_items()

        # 체크리스트 출력
        if st.session_state['checklist']:
            to_update = False  # 체크박스 상태 변경 시 트리거

            for idx, item in enumerate(st.session_state['checklist']):
                col1_1, col1_2 = st.columns([6, 1])
                with col1_1:
                    # 고유한 키를 사용하여 체크박스 생성
                    checkbox_key = f"item_{item.item}_{item.deadline}_{idx}"
                    completed_status = st.checkbox(
                        " ", 
                        key=checkbox_key, 
                        value=item.completed
                    )

                    # 스타일 적용 및 텍스트 출력
                    label_style = "completed" if completed_status else ""
                    st.markdown(
                        f"<div class='checklist-item'>"
                        f"<span class='{label_style}'>{item.item} "
                        f"({item.deadline.strftime('~%Y-%m-%d')})</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    if completed_status != item.completed:
                        self.service.update_item(item.id, completed_status)
                        to_update = True

                with col1_2:
                    # Streamlit 버튼만 사용 (CSS로 스타일 적용)
                    delete_button_clicked = st.button(
                        label="삭제",  # 버튼 텍스트
                        key=f"delete_{idx}",  # 고유 키
                    )
                    # 버튼 클릭 시 해당 항목 삭제
                    if delete_button_clicked:
                        self.service.delete_item(item.id)
                        st.session_state['checklist'] = self.service.get_all_items()
                        to_update = True

            # 상태 변경 시 리스트 재정렬
            if to_update:
                st.session_state['checklist'] = self.service.get_all_items()
                st.rerun()