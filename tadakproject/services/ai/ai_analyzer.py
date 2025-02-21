# services/ai/ai_analyzer.py

from typing import List, Dict
from services.ai.clova_executor import CompletionExecutor

class AIAnalyzer:
    def __init__(self):
        self.executor = CompletionExecutor()

    def analyze_person(self, person: str, text: str) -> str:
        system_prompt =f'''
            - 주어진 텍스트에서 {person}의 특징에 대해 분석합니다.
            -중복되거나 비슷한 맥락의 특징은 하나만 작성하세요.
            - 1~3가지 특징을 한 줄에 하나씩 작성해주세요.
            - 다음과 같은 말투로 30자 이내로 출력하세요. :
            ">{person} 님은 ~한 경향이 있어요!\n"
            ">{person} 님은 최근 ~한 업무를 진행한 것 같아요.\n"
            ">{person} 님은 ~한 이력이 잦아요.\n"
            ">{person} 님은 주로 ~할 확률이 높아요.\n"
        '''
        
        return self._generate_response(system_prompt, text)

    def generate_suggestions(self, data: str) -> str:
        system_prompt = """
        최근 데이터를 분석하여 다음과 같은 형식으로 제안사항을 생성하세요:
        -출력형식: "**❗ 앗, 미리 준비해주세요!** \n", 내용: 다가오는 회의나 일정에 대한 준비사항
        -출력형식: "**🤝 팀원들과 이렇게 작업해봐요.**\n", 내용: 팀원들의 선호도를 고려한 협업 제안
        -출력형식: "**📈 업무 효율을 높이려면...** \n", 내용: 업무 패턴을 바탕으로 한 효율성 향상 조언
        최대한 간결하게 작성해주세요(항목당 제안사항 2개, 제안사항 개당 분량 50자 이내).
        제안사항은 한 줄에 하나씩 작성해주세요.
        무조건 세 가지 제안사항을 모두 반환하세요.
        
        """
        
        return self._generate_response(system_prompt, data)

    def generate_recommendations(self, skills: List[str], project_keywords: List[str],
                               news: List[Dict], tutorials: List[Dict]) -> str:
        system_prompt = """
        현재 프로젝트 데이터를 바탕으로 다음을 추천해주세요:
        -출력형식: "**📖 최근 진행한 프로젝트에 이런 기술이 중요해요.** \n", 내용: 프로젝트 수행에 도움될 만한 기술 스택
        추천항목에 설명을 덧붙이지 말고 최대한 간결하게 작성해주세요.
        """
        
        context = {
            'skills': skills,
            'projects': project_keywords,
            'news': news,
            'tutorials': tutorials
        }
        
        return self._generate_response(system_prompt, str(context))

    def _generate_response(self, system_prompt: str, content: str) -> str:
        preset_text = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ]
        
        request_data = {
            'messages': preset_text,
            'topP': 0.7,
            'maxTokens': 512,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'includeAiFilters': True,
            'seed': 0
        }
        
        return self.executor.execute(request_data)