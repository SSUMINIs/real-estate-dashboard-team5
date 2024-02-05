# -*-coding:utf-8-*-

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd

import streamlit as st

st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣", disabled=True)
st.page_link("http://www.google.com", label="Google", icon="🌎")

# 데이터 로드 및 필터링
data = pd.read_csv('data/processed_full_data.csv')

# 데이터 준비
current_year = pd.to_datetime('today').year
data['Building Age'] = current_year - data['BUILD_YEAR']
data['Age Category'] = data['Building Age'].apply(lambda x: '20년 이상' if x >= 20 else '20년 미만')

# 탭 및 사이드바 구성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["노후 건물 분포도", "노후 건물 거래 동향", "탭 3", "탭 4", "탭 5"])

with tab1:
  st.header("서울시 구별 건축년도에 따른 노후 건물 분포도")
  
  # 구별로 데이터를 집계
  district_age_data = data.groupby(['SGG_NM', 'Age Category']).size().reset_index(name='Count')
  
  # 막대 그래프 시각화
  fig = px.bar(
      district_age_data,
      x='SGG_NM',
      y='Count',
      color='Age Category',
      title='구별 노후 건물 분포',
      labels={'Count': '건물 수', 'SGG_NM': '서울시 구', 'Age Category': '노후 정도'},
      barmode='group'
  )
  
  # 그래프 레이아웃 설정
  fig.update_layout(
      xaxis_title='서울시 구',
      yaxis_title='건물 수',
      plot_bgcolor='white',
      xaxis={'categoryorder':'total descending'},
      legend_title_text='노후 정도'
  )
  
  st.plotly_chart(fig)


# 건축년도를 기준으로 20년 이상된 건물만 필터링
old_buildings = data[data['BUILD_YEAR'] <= (current_year - 20)]


# 사이드바에서 구 선택
selected_district = st.sidebar.selectbox("구 선택", data['SGG_NM'].unique())

with tab2:
    st.header("구별 건물용도, 건축년도, 거래량 비교")

    # 20년 이상된 건물 필터링 및 선택된 구에 대한 데이터 필터링
    filtered_data = data[(data['BUILD_YEAR'] <= (current_year - 20)) & (data['SGG_NM'] == selected_district)]
    
    # 건물용도별 거래량 계산
    transaction_by_type = filtered_data['HOUSE_TYPE'].value_counts().reset_index()
    transaction_by_type.columns = ['HOUSE_TYPE', 'TRANSACTION_COUNT']
  
    # 시각화
    fig = px.bar(
        transaction_by_type,
        x='HOUSE_TYPE',
        y='TRANSACTION_COUNT',
        title=f'{selected_district} 구별 건물용도별 거래량',
        labels={'HOUSE_TYPE': '건물용도', 'TRANSACTION_COUNT': '거래량'},
        color='HOUSE_TYPE'
    )
    st.plotly_chart(fig)