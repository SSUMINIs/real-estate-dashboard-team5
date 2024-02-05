import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk

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
data_unique['Age Category'] = data_unique['BUILD_YEAR'].apply(lambda x: '20년 이상' if current_year - x >= 20 else '20년 미만')

# 20년 이상 된 건물만 필터링
old_buildings = data_unique[data_unique['Age Category'] == '20년 이상']

# 건물 유형별 및 구별 거래량 계산
transaction_by_type_and_district = old_buildings.groupby(['SGG_NM', 'HOUSE_TYPE']).size().reset_index(name='TRANSACTION_COUNT')

# 시각화
fig = px.bar(
    transaction_by_type_and_district, 
    x="SGG_NM", 
    y="TRANSACTION_COUNT", 
    color="HOUSE_TYPE", 
    title="서울시 구별 건물 유형별 거래량", 
    labels={'SGG_NM': '구', 'TRANSACTION_COUNT': '거래량', 'HOUSE_TYPE': '건물 유형'}
)

# Streamlit에서 그래프 표시
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

if selected_district == '전체':
    # 시각화
    fig = px.bar(
        transaction_by_type,
        x='HOUSE_TYPE',
        y='TRANSACTION_COUNT',
        title='서울시 건물 유형별 거래량',
        labels={'HOUSE_TYPE': '건물 유형', 'TRANSACTION_COUNT': '거래량'},
        color='HOUSE_TYPE'
        )
    st.plotly_chart(fig)
else:
    # 시각화
    fig = px.bar(
        transaction_by_type,
        x='HOUSE_TYPE',
        y='TRANSACTION_COUNT',
        title=f'{selected_district} 건물 유형별 거래량',
        labels={'HOUSE_TYPE': '건물 유형', 'TRANSACTION_COUNT': '거래량'},
        color='HOUSE_TYPE'
        )
    st.plotly_chart(fig)


def get_get_top_districts():
    # '구'와 '동'을 결합하여 고유한 지역명 생성
    old_buildings['DISTRICT'] = old_buildings['SGG_NM'] + ' ' + old_buildings['BJDONG_NM']

    # 고유 지역명 별로 노후 건물의 수 계산
    building_counts_by_district = old_buildings.groupby('DISTRICT').size().reset_index(name='OLD_BUILDING_COUNT')

    # 노후 건물이 많은 상위 3개 지역 선택
    top_districts = building_counts_by_district.nlargest(3, 'OLD_BUILDING_COUNT')
    return top_districts

top3_districts = get_get_top_districts()

# 시각화
fig = px.bar(
    top3_districts, 
    x='DISTRICT', 
    y='OLD_BUILDING_COUNT', 
    text='OLD_BUILDING_COUNT',
    title='노후 건물이 밀집한 상위 3개 지역', 
    labels={'OLD_BUILDING_COUNT': '노후 건물 수', 'DISTRICT': '지역'},
    color='DISTRICT'
)

st.plotly_chart(fig)
