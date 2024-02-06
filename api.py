# import requests
# from dotenv import load_dotenv
# import os

# # 크롤링 함수 정의
# def get_news_data(query, max_results=3):
#     load_dotenv()

#     # 임시 하드코딩된 클라이언트 ID와 클라이언트 시크릿 사용
#     client_id = "OwearAQmAQTwgoPJ_ONT"
#     client_secret = "e2nj2FiBR_"
    
#     url = "https://openapi.naver.com/v1/search/news.json"
#     headers = {
#         "X-Naver-Client-Id": client_id,
#         "X-Naver-Client-Secret": client_secret
#     }

#     params = {
#         "query": query,
#         "sort": "sim",
#         "start": 1,
#         "display": 5
#     }

#     response = requests.get(url, headers=headers, params=params)

#     # API 요청 및 응답 처리
#     if response.status_code == 200:
#         news_data = response.json()
#         return news_data['items'][:max_results]  # 상위 3개 결과만 반환
#     else:
#         return None

