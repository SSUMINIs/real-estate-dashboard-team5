import streamlit as st
import pandas as pd
import plotly.express as px

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
data_unique['Age Category'] = data_unique['BUILD_YEAR'].apply(lambda x: '20년 이상' if current_year - x >= 20 else '20년 미만')

# 구별 및 연령 범주별 건물 수 계산
building_counts = data_unique.groupby(['SGG_NM', 'Age Category']).size().reset_index(name='Building Count')

# 전체 건물 수를 기준으로 내림차순 정렬
building_counts_sorted = building_counts.sort_values(by='Building Count', ascending=False)

# 구별 건물 수 시각화
fig = px.bar(
    building_counts_sorted,
    x='SGG_NM',
    y='Building Count',
    color='Age Category',
    title='구별 건물 수 (20년 이상, 20년 미만)',
    labels={'Building Count': '건물 수', 'SGG_NM': '구', 'Age Category': '건물 연령 범주'},
    barmode='group'
)

st.plotly_chart(fig)

# 사이드바 구 선택
selected_district = st.sidebar.selectbox("구 선택", ['전체'] + sorted(data_unique['SGG_NM'].unique()))

# 선택된 구에 따른 동 선택
if selected_district != '전체':
    selected_dong = st.sidebar.selectbox("동 선택", ['전체'] + sorted(data_unique[data_unique['SGG_NM'] == selected_district]['BJDONG_NM'].unique()))
else:
    selected_dong = '전체'

# 데이터 필터링
if selected_district != '전체':
    if selected_dong != '전체':
        filtered_data = data_unique[(data_unique['SGG_NM'] == selected_district) & (data_unique['BJDONG_NM'] == selected_dong)]
    else:
        filtered_data = data_unique[data_unique['SGG_NM'] == selected_district]
else:
    filtered_data = data_unique

# 구별 건물 개수 계산
building_counts_by_district = filtered_data['SGG_NM'].value_counts().reset_index()
building_counts_by_district.columns = ['SGG_NM', 'Building Count']

# 시각화
fig = px.bar(
  building_counts_by_district, 
  x='SGG_NM', 
  y='Building Count', 
  title='구별 건물 수'
  )
st.plotly_chart(fig)