import pandas as pd
import streamlit as st
import re
from crawling import get_news_data

st.set_page_config(layout="wide")

# 데이터 불러오기
data_danlist = pd.read_csv('data/단독다가구.csv')
data_yeonlist = pd.read_csv('data/연립다세대.csv')

combined_data = pd.concat([data_danlist, data_yeonlist])

# 화곡동에 해당하는 데이터만 필터링
filtered_data = combined_data[combined_data['BJDONG_NM'] == '화곡동']

# HTML 태그 제거 함수
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

st.markdown('#### 첫번째 근거 이미지')
st.image('images/노후 건물 개수 상위 10개 지역.png', caption='노후 건물 개수 상위 10개 지역')
st.markdown('#### 두번째 근거 이미지')
st.image('images/노후 건물 거래량 상위 10개 지역.png', caption='노후 건물 개수 상위 10개 지역')

# 필드명 한글로 변경
filtered_data = filtered_data.rename(columns={
    'HOUSE_TYPE': '건물유형',
    'PRICE_PER': '평균 평당가격',
    'BJDONG_NM': '법정동 명',
    'SGG_NM': '구 명',
    'CENTER_LONG': '경도',
    'CENTER_LATI': '위도'
})

# 평균 평당가격을 반올림하여 정수로 변환하고 '만원' 단위 붙이기
filtered_data['평균 평당가격'] = filtered_data['평균 평당가격'].round(0).astype(int).astype(str) + "만원"

# 테이블로 표시
st.table(filtered_data)

st.markdown('#### 세번째 근거 이미지')
st.image('images/재개발 선정 지역.png', caption='재개발 선정 지역', width=880)

# 버튼을 사용하여 뉴스 정보 로드
if st.button("관련 정보 가져오기"):
    queries = ['관악구 신림동 재개발', '강북구 수유동 재개발', '관악구 봉천동 재개발', '양천구 신월동 재개발', '강북구 미아동 재개발']
    for query in queries:
        news = get_news_data(query)
        if news:
            st.subheader(f"{query} 관련 뉴스")
            for item in news:
                title = remove_html_tags(item['title'])
                link = item['link']
                st.markdown(f"[{title}]({link})")

