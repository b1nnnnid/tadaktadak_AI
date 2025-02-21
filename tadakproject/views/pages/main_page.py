# views/pages/main_page.py

import time
import streamlit as st
from datetime import date
from services.ai_service import AIService
from views.components.checklist import ChecklistComponent

class MainPageView:
    def __init__(self):
        self.ai_service = AIService()  # AI 서비스 초기화
        
    def render(self):
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📅 캘린더")
            calendar_options = {
                "editable": "true",
                "selectable": "true",
                "headerToolbar": {
                    "left": "title",
                    "center": None,
                    "right": "today,prev,next"
                },
                "slotMinTime": "00:00:00",
                "slotMaxTime": "24:00:00",
                "initialView": "dayGridMonth",
                "resourceGroupField": "building",
                "resources": [
                    {"id": "a", "building": "Building A", "title": "Building A"},
                    {"id": "b", "building": "Building A", "title": "Building B"},
                    {"id": "c", "building": "Building B", "title": "Building C"},
                    {"id": "d", "building": "Building B", "title": "Building D"},
                    {"id": "e", "building": "Building C", "title": "Building E"},
                    {"id": "f", "building": "Building C", "title": "Building F"},
                ],
                "height": "400px", 
            }
            calendar_events = [
                {
                    "title": "나나 프로젝트 기간 ",
                    "start": "2024-12-10T08:30:00",
                    "end": "2024-12-14T10:30:00",
                    "resourceId": "a",
                },
                {
                    "title": "가가 프로젝트 마감",
                    "start": "2025-01-11T23:30:00",
                    "end": "2023-01-13T23:30:00",
                    "resourceId": "b",
                },
                {
                    "title": "다다 프로젝트 회의",
                    "start": "2024-12-01T10:40:00",
                    "end": "2024-12-02T12:30:00",
                    "resourceId": "c",
                }
            ]
            custom_css="""
                .fc-event-past {
                    opacity: 0.4;
                }
                .fc-event-time {
                    font-style: italic;
                }
                .fc-event-title {
                    font-weight: 700;
                }
                .fc-toolbar-title {
                    font-size: 1rem;
                    color:#000080; 

                }


                 .fc-button {
                    background-color:#000080; ; /* 버튼 배경색 */
                    color: white; /* 버튼 텍스트 색상 */
                    font-size: 14px; /* 버튼 텍스트 크기 */
                    padding: 3px 10px; /* 버튼 크기 (상하 10px, 좌우 20px) */
                    border-radius: 5px; /* 버튼 모서리 둥글게 */
                    border: none; /* 버튼 테두리 제거 */
                
                }

                .fc-button-primary {
                    background-color: #000080 !important; /* 오늘 버튼 배경색 */
                    color: white !important; /* 오늘 버튼 텍스트 색상 */
                }

                  
            """
            my_calendar = cl(events=calendar_events, options=calendar_options, custom_css=custom_css)
            my_calendar
            st.markdown("<br>", unsafe_allow_html=True)  # <br>를 세 번 사용하여 공백 추가
            st.markdown("<hr>", unsafe_allow_html=True)
            ChecklistComponent().render()

        with col2:
            if st.button("생성"):
                self.ai_service.generate_main_analysis()
                self.ai_service.generate_recommendations()

                # 성공 메시지 출력
                st.success("새로운 AI 조언과 추천 콘텐츠가 생성되었습니다!")
                time.sleep(1)
                # 새로고침으로 최신 데이터를 화면에 반영
                st.rerun()

            # AI 조언
            st.subheader("💡 AI 조언")
            suggestions = self.ai_service.get_latest_analysis("main_suggestions")

            if suggestions["status"] == "success":
                # 성공적으로 데이터를 가져왔을 때
                st.info(suggestions["content"])

            elif suggestions["status"] == "no_data":
                # 데이터가 없을 때 즉시 AI 분석 시작
                st.warning("아직 데이터가 없습니다. AI 분석을 시작합니다...")
                self.ai_service.generate_main_analysis()  # 분석 실행
                st.success("AI 분석이 완료되었습니다. 페이지를 새로고침하세요.")
                st.experimental_rerun()  # 새로고침으로 결과 반영

            else:
                # 데이터가 처리 중일 때
                st.info("데이터를 불러오는 중입니다. 잠시만 기다려주세요...")

            # 추천 콘텐츠
            st.subheader("📚 추천 콘텐츠")
            recommendations = self.ai_service.get_latest_analysis("recommendations")
            if recommendations["status"] == "success":
                content = recommendations["content"]
                if isinstance(content, dict):
                    if content.get('ai_recommendations'):
                        st.write(content['ai_recommendations'])
                    
                    if content.get('news'):
                        st.write("**📖 이런 것들을 참고해보세요.**")
                        for news in content['news']:
                            with st.expander(news['title']):
                                st.write(news['description'])
                                st.markdown(f"[기사 보기]({news['link']})")
                    
                    if content.get('tutorials'):
                        st.write("**📖 공부해두면 도움이 될 거예요!**")
                        for tutorial in content['tutorials']:
                            with st.expander(tutorial['title']):
                                st.write(tutorial['description'])
                                st.markdown(f"[강의 보기]({tutorial['link']})")
                else:
                    # 이전 형식의 데이터 처리
                    st.write(content)