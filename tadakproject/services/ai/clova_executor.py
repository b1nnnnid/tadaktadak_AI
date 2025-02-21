# services/ai/clova_executor.py

import os
import requests

class CompletionExecutor:
    def __init__(self):
        self._host = os.getenv('CLOVA_HOST')
        self._api_key = os.getenv('CLOVA_API_KEY')
        self._api_key_primary_val = os.getenv('CLOVA_API_KEY_PRIMARY')
        self._request_id = os.getenv('CLOVA_REQUEST_ID')

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        }

        with requests.post(
            self._host + '/testapp/v1/chat-completions/HCX-003',
            headers=headers,
            json=completion_request,
            stream=True
        ) as r:
            if r.status_code == 200:
                response_json = r.json()
                print("API 응답:", response_json)
                return response_json['result']['message']['content']
            else:
                return f"Error: {r.status_code}"