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

# 구별 및 건물 유형별 거래량 계산
transactions_by_type_and_district = old_transactions.groupby(['SGG_NM', 'HOUSE_TYPE']).size().reset_index(name='TRANSACTION_COUNT')

# 거래량을 기준으로 내림차순 정렬
transactions_by_type_and_district_sorted = transactions_by_type_and_district.sort_values(by=['SGG_NM', 'TRANSACTION_COUNT'], ascending=[True, False])

# 시각화
fig = px.bar(
    transactions_by_type_and_district_sorted, 
    x="SGG_NM", 
    y="TRANSACTION_COUNT", 
    color="HOUSE_TYPE",
    title="서울시 건물유형별 노후 건물 거래량",
    labels={'SGG_NM': '구', 'TRANSACTION_COUNT': '거래량', 'HOUSE_TYPE': '건물 유형'},
    barmode='stack'
)
st.plotly_chart(fig)

# 'DISTRICT' 열 생성
old_transactions['DISTRICT'] = old_transactions['SGG_NM'] + ' ' + old_transactions['BJDONG_NM']

# 사이드바 설정
district_options = ['노후 건물 거래량 상위 10개 지역'] + sorted(old_transactions['SGG_NM'].unique())
selected_district = st.sidebar.selectbox("구 선택", district_options)

default_types = ['연립다세대', '단독다가구']
selected_house_types = st.sidebar.multiselect("건물 유형 선택", old_transactions['HOUSE_TYPE'].unique(), default=default_types)

# 데이터 필터링 및 시각화
if selected_district != '노후 건물 거래량 상위 10개 지역':
    # 해당 구와 선택된 건물 유형에 해당하는 데이터 필터링
    filtered_data = old_transactions[(old_transactions['SGG_NM'] == selected_district) & (old_transactions['HOUSE_TYPE'].isin(selected_house_types))]
    
    # 'DISTRICT' 별로 거래량 계산 및 내림차순 정렬
    transactions_by_district = filtered_data.groupby('DISTRICT').size().reset_index(name='TRANSACTION_COUNT')
    transactions_by_district_sorted = transactions_by_district.sort_values(by='TRANSACTION_COUNT', ascending=False)
        
    fig = px.bar(
        transactions_by_district_sorted,
        x='DISTRICT',
        y='TRANSACTION_COUNT',
        text='TRANSACTION_COUNT',
        title=f'{selected_district} 지역 별 노후 건물 거래량',
        labels={'DISTRICT': '지역', 'TRANSACTION_COUNT': '노후 건물 거래량'},
        color='DISTRICT'
    )
    st.plotly_chart(fig)
else:
    # 전체 데이터에서 건물 유형을 고려하여 'DISTRICT' 별 노후 건물 거래량 계산
    filtered_data = old_transactions[old_transactions['HOUSE_TYPE'].isin(selected_house_types)]
    building_counts_by_district = filtered_data.groupby('DISTRICT').size().reset_index(name='TRANSACTION_COUNT')
    top10_districts = building_counts_by_district.nlargest(10, 'TRANSACTION_COUNT')

    fig = px.bar(
        top10_districts,
        x='DISTRICT',
        y='TRANSACTION_COUNT',
        text='TRANSACTION_COUNT',
        title='노후 건물 거래량이 가장 많은 상위 10개 지역',
        labels={'DISTRICT': '지역', 'TRANSACTION_COUNT': '노후 건물 거래량'},
        color='DISTRICT'
    )
    st.plotly_chart(fig)

# 크롤링 함수 불러오기
# from api import get_news_data
    
