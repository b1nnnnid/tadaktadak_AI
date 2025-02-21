import os
from typing import List, Dict
import requests
from urllib.parse import quote
import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()

class ContentFinder:
    def __init__(self):
        self.naver_client_id = os.getenv('NAVER_CLIENT_ID')
        self.naver_client_secret = os.getenv('NAVER_CLIENT_SECRET')
        self.youtube = googleapiclient.discovery.build(
            'youtube', 'v3',
            developerKey=os.getenv('YOUTUBE_API_KEY')
        )
        # 초기화 시 API 키 확인
        print(f"Naver Client ID exists: {bool(self.naver_client_id)}")
        print(f"Naver Client Secret exists: {bool(self.naver_client_secret)}")
        print(f"YouTube API initialized: {bool(self.youtube)}")

    def search_news(self, keywords: List[str], display: int = 3) -> List[Dict]:
        news_results = []
        try:
            print(f"Searching news for keywords: {keywords}")
            for keyword in keywords:
                url = f"https://openapi.naver.com/v1/search/news.json?query={quote(keyword)}&display={display}"
                
                headers = {
                    "X-Naver-Client-Id": self.naver_client_id,
                    "X-Naver-Client-Secret": self.naver_client_secret
                }
                
                print(f"Making request to Naver API for keyword: {keyword}")
                response = requests.get(url, headers=headers)
                print(f"Naver API response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"Found {len(result.get('items', []))} news items")
                    news_results.extend([
                        {
                            'title': item['title'].replace('<b>', '').replace('</b>', ''),
                            'description': item['description'].replace('<b>', '').replace('</b>', ''),
                            'link': item['link'],
                            'pub_date': item['pubDate']
                        }
                        for item in result['items']
                    ])
                else:
                    print(f"Error response from Naver: {response.text}")
        except Exception as e:
            print(f"Error in search_news: {str(e)}")
        
        return news_results[:3]

    def search_tutorials(self, skills: List[str], max_results: int = 3) -> List[Dict]:
        tutorial_results = []
        try:
            print(f"Searching tutorials for skills: {skills}")
            for skill in skills:
                try:
                    print(f"Making YouTube API request for skill: {skill}")
                    search_response = self.youtube.search().list(
                        q=skill + " tutorial",
                        part="snippet",
                        maxResults=max_results,
                        type="video",
                        relevanceLanguage="ko",
                        order="relevance"
                    ).execute()

                    print(f"Found {len(search_response.get('items', []))} tutorial items")
                    tutorial_results.extend([
                        {
                            'title': item['snippet']['title'],
                            'description': item['snippet']['description'],
                            'thumbnail': item['snippet']['thumbnails']['default']['url'],
                            'video_id': item['id']['videoId'],
                            'link': f"https://youtube.com/watch?v={item['id']['videoId']}"
                        }
                        for item in search_response.get('items', [])
                    ])
                except Exception as e:
                    print(f"YouTube API error for skill {skill}: {str(e)}")
        except Exception as e:
            print(f"Error in search_tutorials: {str(e)}")
        
        return tutorial_results[:3]