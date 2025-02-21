# services/ai_service.py

from datetime import datetime
from typing import List, Dict
from config.database import DatabaseConfig
from services.ai.ai_analyzer import AIAnalyzer
from services.ai.content_finder import ContentFinder
from services.coworkers_services import CoworkersService

class AIService:
    def __init__(self):
        self.analyzer = AIAnalyzer()
        self.content_finder = ContentFinder()
        print(f"ContentFinder 초기화 확인: {self.content_finder}")
        self.conn = DatabaseConfig.get_connection()
        self.personnel_service = CoworkersService

    def analyze_person(self, person: str, text: str) -> str:
        mentions = self.personnel_service.get_mentioned_content(person)
        if mentions:
            for mention in mentions:
                mention_text = f"{mention['meeting_content']} {mention['action_items']} {mention['special_notes']}"
        result = self.analyzer.analyze_person(person, mention_text)
        self._save_insight("person_analysis", result, "person", person)
        return result

    
    def analyze_person_mentions(self, person_name: str, meeting_logs: List[Dict])->str:
        """
        특정 인물에 대한 회의록 분석
        :param person_name: 분석할 인물 이름
        :param meeting_logs: 회의록 데이터 리스트
        :return: 분석 결과 문자열
        """
        mentions = [log for log in meeting_logs if person_name in log["meeting_content"]]
        if not mentions:
            return f"{person_name}님은 회의록에서 언급되지 않았습니다."

        summary = self.analyze_person(person_name,mentions)

        # 결과 저장
        self._save_insight("person_mentions", summary, "meeting_logs", person_name)
        return summary
    
    
    def generate_main_suggestions(self, recent_data: str) -> str:
        result = self.analyzer.generate_suggestions(recent_data)
        self._save_insight("main_suggestions", result, "general", "main")
        return result

    def get_enriched_recommendations(self, skills: List[str], 
                                   project_keywords: List[str]) -> Dict:
        news_results = self.content_finder.search_news(project_keywords)
        tutorial_results = self.content_finder.search_tutorials(skills)
        
        recommendations = self.analyzer.generate_recommendations(
            skills, project_keywords, news_results, tutorial_results
        )
        
        self._save_insight(
            "content_recommendations",
            recommendations,
            "project",
            "learning"
        )
        
        return {
            'ai_recommendations': recommendations,
            'news': news_results,
            'tutorials': tutorial_results
        }

    def _save_insight(self, type: str, content: str, source_type: str, source_id: str):
        cursor = self.conn.cursor()
        current_time = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO insights (
                created_at, type, content, source_type, source_id, source_created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (current_time, type, content, source_type, source_id, current_time))
        self.conn.commit()
        
    
    # main page AI 반환값 관련
    def generate_main_analysis(self):
        """AI 조언 생성 및 저장"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        try:
            # 최근 데이터를 가져와 AI 분석 수행
            recent_data = self._get_recent_meeting_data()  # 최근 데이터를 가져오는 메서드
            content = self.analyzer.generate_suggestions(recent_data)  # AI로 결과 생성

            # 생성된 결과를 데이터베이스에 저장
            cursor.execute("""
                INSERT INTO main_ai_results (type, content)
                VALUES (?, ?)
            """, ("main_suggestions", content))
            conn.commit()
        finally:
            conn.close()

    def generate_recommendations(self):
        """추천 콘텐츠 생성 및 저장"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        try:
            # AI 분석에 필요한 데이터 준비
            skills = self._get_current_skills()
            project_keywords = self._get_current_projects()
            news = self.content_finder.search_news(project_keywords)
            tutorials = self.content_finder.search_tutorials(skills)

            # AI 추천 생성
            ai_recommendations = self.analyzer.generate_recommendations(
                skills, 
                project_keywords, 
                news, 
                tutorials
            )

            # 전체 결과를 딕셔너리로 구성
            content = {
                'ai_recommendations': ai_recommendations,
                'news': news,
                'tutorials': tutorials
            }

            # JSON 형태로 변환하여 저장
            import json
            cursor.execute("""
                INSERT INTO main_ai_results (type, content)
                VALUES (?, ?)
            """, ("recommendations", json.dumps(content)))
            conn.commit()

        except Exception as e:
            print(f"Error in generate_recommendations: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def get_latest_analysis(self, analysis_type: str):
        """최근 데이터를 가져옵니다."""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT content, created_at
                FROM main_ai_results
                WHERE type = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (analysis_type,))
            result = cursor.fetchone()
            
            if not result:
                return {"status": "no_data", "message": "데이터가 없습니다."}

            content, created_at = result
            
            # recommendations 타입인 경우 JSON 파싱
            if analysis_type == "recommendations":
                try:
                    import json
                    content = json.loads(content)
                except json.JSONDecodeError:
                    # 이전 형식의 데이터는 그대로 반환
                    content = {"ai_recommendations": content}
            
            return {"status": "success", "content": content, "created_at": created_at}
        finally:
            conn.close()
    
    def _get_current_skills(self) -> list:
        """현재 필요한 기술 스택 반환"""
        return ["Python", "데이터 분석", "SQL"]

    def _get_current_projects(self) -> list:
        """현재 진행 중인 프로젝트 키워드 반환"""
        return ["빅데이터 분석", "AI 프로젝트"]

    # 보조 메서드: 최근 회의 데이터 가져오기
    def _get_recent_meeting_data(self) -> str:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT meeting_content, action_items
                FROM meeting_logs
                ORDER BY meeting_date DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                return f"{row[0]} {row[1]}"
            else:
                return "회의 데이터가 없습니다."
        finally:
            conn.close()
