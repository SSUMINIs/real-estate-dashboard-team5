# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import geopandas as gpd
import json
import numpy as np
import pydeck as pdk
# from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

# 데이터 로드 및 필터링
data = pd.read_csv("data/Seoul_data.csv")
seoul_gpd = gpd.read_file("data/seoul_sig_cd.geojson")

# 데이터 준비
current_year = pd.to_datetime('today').year
data['Building Age'] = current_year - data['BUILD_YEAR']
data['Age Category'] = data['Building Age'].apply(lambda x: '20년 이상' if x >= 20 else '20년 미만')

unique_combin = data.drop_duplicates(subset=['SGG_CD', 'BJDONG_CD','BLDG_NM','BUILD_YEAR'],keep='first').copy()
unique_combin = unique_combin.reset_index(drop=True)

st.header("노후건물(20년이상) 평균 건축년도 및 표준편차")

#서울시 위치 가져오기
tab1_df20 = unique_combin[unique_combin['Age Category']=='20년 이상'].copy()
seoul_gpd = seoul_gpd.set_crs(epsg='5178', allow_override=True)
seoul_gpd['center_point'] = seoul_gpd['geometry'].geometry.centroid
seoul_gpd['geometry'] = seoul_gpd['geometry'].to_crs(epsg=4326) #기본 좌표계를 사용함
seoul_gpd['center_point'] = seoul_gpd['center_point'].to_crs(epsg=4326)
seoul_gpd['경도'] = seoul_gpd['center_point'].map(lambda x: x.xy[0][0])
seoul_gpd['위도'] = seoul_gpd['center_point'].map(lambda x: x.xy[1][0])

seoul_gpd = seoul_gpd.rename(columns={"SIG_CD":"SGG_CD"})
tab1_df20['SGG_CD'] = tab1_df20['SGG_CD'].astype(str)
seoul_gpd = seoul_gpd[['SGG_CD','SIG_KOR_NM','geometry']].reset_index(drop=True)

tab1_df = tab1_df20.groupby('SGG_CD')['Building Age'].agg(['mean','std','size']).reset_index()
tab1_df1= seoul_gpd.merge(tab1_df, on = 'SGG_CD')
tab1_data = tab1_df1.explode(index_parts=True).reset_index(drop=True)

with open('data/seoul.geojson', encoding='UTF-8') as f:
    gpd_data = json.load(f)
    fig = px.choropleth_mapbox(tab1_data, geojson = gpd_data, locations='SIG_KOR_NM', color = 'mean',
                            color_continuous_scale="reds", featureidkey = 'properties.SIG_KOR_NM', #YlOrRd
                            mapbox_style="carto-positron", zoom=9.5, center = {'lat':37.563383, 'lon':126.996039}, #open-street-map ,carto-positron,white-bg
                            opacity=0.5, labels={'meand':'서울시 노후건물 분포도(년)'},custom_data=['std'])

    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},width=1200)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>노후 건물 평균 년도: %{z:,.0f}(년)<br>표준편차: %{customdata:,.0f}')
    fig.update_coloraxes(colorbar_tickformat='000')

    st.plotly_chart(fig)

gu_info = tab1_df20.groupby('SGG_NM').size().reset_index(name='size')
result_df = pd.merge(tab1_df, gu_info, on='size')

fig_mean = px.bar(
        result_df,
        x='SGG_NM',
        y='mean',
        title='구별 평균 건축년도 비교',
        labels={'SGG_NM': '서울시 구', 'mean': '평균 노후정도'},
        width=1100,
        height=500
    )
fig_mean.update_traces(marker_color='darkgrey')

st.plotly_chart(fig_mean)

fig_std = px.bar(
        result_df,
        x='SGG_NM',
        y='std',
        title='구별 평균 건축년도 표준편차',
        labels={'SGG_NM': '서울시 구', 'mean': '표준편차'},
        width=1100,
        height=500
    )
fig_std.update_traces(marker_color='brown') #burlywood chocolate, coral, cornflowerblue, cornsi
st.plotly_chart(fig_std)

# 구별로 데이터를 집계
district_age_data = unique_combin.groupby(['SGG_NM', 'BJDONG_NM','Age Category']).size().reset_index(name='Count')

#사이드바
district_options = ['전체'] + district_age_data['SGG_NM'].unique().tolist()
selected_gu_option = st.sidebar.selectbox("구 선택", district_options)

if selected_gu_option == '전체':
    filtered_data = district_age_data
    st.header("서울시 전체 건물년도 비교(개수)")
    x_value = 'SGG_NM'
    y_value = filtered_data.groupby(['SGG_NM','Age Category'])['Count'].sum().reset_index() 
    bargroupgap_value = 0.1
    
else:
    district_gu_options = ['전체'] + district_age_data.loc[district_age_data['SGG_NM'] == selected_gu_option]['BJDONG_NM'].unique().tolist()
    selected_dong_option = st.sidebar.selectbox("동 선택",  district_gu_options, key=f"{selected_gu_option}_dong")
    
    if selected_dong_option == '전체':
        filtered_data = district_age_data[district_age_data['SGG_NM'] == selected_gu_option]
        st.header(f"{selected_gu_option} 전체 동 건물년도 비교(개수)")
        x_value = 'BJDONG_NM'
        y_value = filtered_data[(filtered_data['SGG_NM'] == selected_gu_option)].groupby(['SGG_NM', 'BJDONG_NM', 'Age Category'])['Count'].sum().reset_index()
        bargroupgap_value = 0.1
    else:
        @st.cache_data
        def load_data(selected_gu_option, selected_dong_option):
            filtered_data = district_age_data[(district_age_data['SGG_NM'] == selected_gu_option) & (district_age_data['BJDONG_NM'] == selected_dong_option)]
            return filtered_data
        # 데이터 로드
        filtered_data = load_data(selected_gu_option, selected_dong_option)
        st.header(f"{selected_gu_option} {selected_dong_option} 건물년도 비교(개수)")
        x_value = 'BJDONG_NM'
        y_value = filtered_data.groupby(['SGG_NM','BJDONG_NM','Age Category'])['Count'].sum().reset_index() 
        bargroupgap_value = 0.5
    
#막대 그래프 시각화
fig = px.bar(
        y_value,
        x=x_value,
        y='Count',
        color='Age Category',
        labels={'Count': '건물 수', x_value: '서울시 동' if selected_gu_option != '전체' else '서울시 구', 'Age Category': '노후 정도'},
        barmode='group'
        )

# 그래프 레이아웃 설정
fig.update_layout(
        xaxis_title=f'{selected_gu_option if selected_gu_option != "전체" else "서울시 구"}',
        yaxis_title='건물 수',
        plot_bgcolor='white',
        xaxis={'categoryorder':'total descending'},
        legend_title_text='노후 정도',
        width=1200,
        height=500,
        bargroupgap=bargroupgap_value 
    )
    
st.plotly_chart(fig)

# 20년 이상, 구>동 건물개수 상위 10개
st.header("노후 건물 개수 상위 10개 지역")
district_age_data = unique_combin.groupby(['SGG_NM', 'BJDONG_NM','Age Category']).size().reset_index(name='Count')

# '20년 이상' 필터링 및 내림차순 정렬
dong_10 = district_age_data[district_age_data['Age Category'] == '20년 이상'].nlargest(10, 'Count')

# 'Name' 열 추가
dong_10['Name'] = dong_10['SGG_NM'] + ' ' + dong_10['BJDONG_NM']

# 시각화
fig = px.bar(
    dong_10,  # 수정된 데이터프레임 사용
    x="Name", 
    y="Count", 
    color='SGG_NM', 
    labels={'Name': '지역', 'Count': '노후 건물수', 'SGG_NM' : '지역'},
    text="Count",
    width=1200,
    height=500
)

#x축 정렬 설정
fig.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig)
