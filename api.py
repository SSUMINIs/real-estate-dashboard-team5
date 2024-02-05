import requests
from dotenv import load_dotenv
import os
from pages.노후 건물 거래 동향 import get_top_districts

load_dotenv()

# 네이버 개발자 센터에서 발급받은 클라이언트 ID와 클라이언트 시크릿
client_id = os.getenv('NAVER_client_id')
client_secret = os.getenv('NAVER_client_secret')

# 검색어 설정
query = "화곡동 재개발"

# API 요청 URL 및 헤더
url = "https://openapi.naver.com/v1/search/news.json"
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

# 파라미터에 검색어 및 추가 파라미터 설정
params = {
    "query": query,  # 검색어
    "sort": "sim",  # 정렬 방식: date(최신순), sim(유사도순)
    "start": 1,  # 검색 결과의 시작 위치 (기본값 1)
    "display": 5  # 반환되는 검색 결과의 수 (최대 100)
}

# API 요청
response = requests.get(url, headers=headers, params=params)

# 응답 결과 확인 (JSON 형식)
if response.status_code == 200:
    news_data = response.json()
    print(news_data)  # JSON 형식의 뉴스 검색 결과 출력
else:
    print("Error Code:", response.status_code)