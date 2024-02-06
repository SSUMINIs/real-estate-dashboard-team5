import streamlit as st
import pandas as pd
import plotly.express as px

# header
st.header("노후 건물 거래 동향")

# 데이터 로드 및 필터링
data = pd.read_csv("data/Seoul_data.csv")

# 건물명이 누락된 경우 처리
data['BLDG_NM'].fillna('Unknown', inplace=True)

# 고유 식별자 생성 및 중복 제거
data['unique_id'] = data['SGG_NM'] + data['BJDONG_NM'] + data['BLDG_NM'] + data['BUILD_YEAR'].astype(str)
data_unique = data.drop_duplicates(subset='unique_id')

# 현재 년도 정의
current_year = 2024

# '20년 이상', '20년 미만' 범주화
data['Age Category'] = data['BUILD_YEAR'].apply(lambda x: '20년 이상' if current_year - x >= 20 else '20년 미만')
data_unique['Age Category'] = data_unique['BUILD_YEAR'].apply(lambda x: '20년 이상' if current_year - x >= 20 else '20년 미만')

# 20년 이상 된 건물만 필터링
old_buildings = data_unique[data_unique['Age Category'] == '20년 이상']

# 20년 이상된 건물의 거래만 고려
old_transactions = data[data['Age Category'] == '20년 이상']

# 구별 거래량 계산 (DEAL_YMD 포함하지 않음)
transactions_by_district = old_transactions.groupby('SGG_NM').size().reset_index(name='TRANSACTION_COUNT')

# 거래량을 기준으로 내림차순 정렬
transactions_by_district_sorted = transactions_by_district.sort_values(by='TRANSACTION_COUNT', ascending=False)

# 시각화
fig = px.bar(
    transactions_by_district_sorted, 
    x="SGG_NM", 
    y="TRANSACTION_COUNT", 
    title="서울시 구별 노후 건물 거래량", 
    labels={'SGG_NM': '구', 'TRANSACTION_COUNT': '거래량'},
)
st.plotly_chart(fig)


# 사이드바에서 구 선택
selected_district = st.sidebar.selectbox("구 선택", ['전체'] + list(old_buildings['SGG_NM'].unique()))

# 사이드바에서 여러 건물 유형 선택
selected_house_types = st.sidebar.multiselect("건물 유형 선택", old_buildings['HOUSE_TYPE'].unique(), default=old_buildings['HOUSE_TYPE'].unique())

# 선택된 구에 따른 데이터 필터링
if selected_district != '전체':
    filtered_data = old_buildings[old_buildings['SGG_NM'] == selected_district]
else:
    filtered_data = old_buildings
    
# 선택된 건물 유형에 따른 데이터 필터링
if selected_house_types:
    filtered_data = filtered_data[filtered_data['HOUSE_TYPE'].isin(selected_house_types)]

# 건물 유형별 거래량 계산
transaction_by_type = filtered_data['HOUSE_TYPE'].value_counts().reset_index()
transaction_by_type.columns = ['HOUSE_TYPE', 'TRANSACTION_COUNT']

# 추가적인 시각화
if selected_district == '전체':
    fig = px.bar(
        transaction_by_type,
        x='HOUSE_TYPE',
        y='TRANSACTION_COUNT',
        title='서울시 건물 유형별 거래량',
        labels={'HOUSE_TYPE': '건물 유형', 'TRANSACTION_COUNT': '거래량'},
        color='HOUSE_TYPE'
    )
else:
    fig = px.bar(
        transaction_by_type,
        x='HOUSE_TYPE',
        y='TRANSACTION_COUNT',
        title=f'{selected_district} 건물 유형별 거래량',
        labels={'HOUSE_TYPE': '건물 유형', 'TRANSACTION_COUNT': '거래량'},
        color='HOUSE_TYPE'
    )
st.plotly_chart(fig)

# 노후 밀집도가 높은 10개 지역 구하기
old_buildings['DISTRICT'] = old_buildings['SGG_NM'] + ' ' + old_buildings['BJDONG_NM']
building_counts_by_district = old_buildings.groupby('DISTRICT').size().reset_index(name='OLD_BUILDING_COUNT')
top10_districts = building_counts_by_district.nlargest(10, 'OLD_BUILDING_COUNT')

# 시각화
fig = px.bar(
    top10_districts, 
    x='DISTRICT', 
    y='OLD_BUILDING_COUNT', 
    text='OLD_BUILDING_COUNT',
    title='노후 건물이 밀집한 상위 10개 지역', 
    labels={'OLD_BUILDING_COUNT': '노후 건물 수', 'DISTRICT': '지역'},
    color='DISTRICT'
)
st.plotly_chart(fig)

# 노후 밀집도가 높은 3개 지역 구하기
old_buildings['DISTRICT'] = old_buildings['SGG_NM'] + ' ' + old_buildings['BJDONG_NM']
building_counts_by_district = old_buildings.groupby('DISTRICT').size().reset_index(name='OLD_BUILDING_COUNT')
top3_districts = building_counts_by_district.nlargest(3, 'OLD_BUILDING_COUNT')

# 시각화
fig = px.bar(
    top3_districts, 
    x='DISTRICT', 
    y='OLD_BUILDING_COUNT', 
    text='OLD_BUILDING_COUNT',
    title='노후 건물이 밀집한 상위 10개 지역', 
    labels={'OLD_BUILDING_COUNT': '노후 건물 수', 'DISTRICT': '지역'},
    color='DISTRICT'
)
st.plotly_chart(fig)


# 크롤링 함수 불러오기
from api import get_news_data

# 관련 정보 가져오기 버튼
if st.button("관련 정보 가져오기"):
    for district in top3_districts['DISTRICT']:
        news_data = get_news_data(district)
        if news_data:
            st.subheader(f"{district} 관련 뉴스")
            for item in news_data:
                st.markdown(f"[{item['title']}]({item['link']})")
        else:
            st.write(f"{district}에 대한 뉴스를 가져오는 데 실패했습니다.")

    
