import streamlit as st
import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd

st.set_page_config(
    layout="wide",  # 더 많은 공간을 위한 넓은 레이아웃 설정
    page_title="당신의 앱 제목",  # 앱 제목 설정
)

# 아이콘을 포함한 페이지 링크 생성
st.page_link("pages/01 Hi There.py", label="Hi There", icon="👋")
st.page_link("pages/02 노후 건물 분포도.py", label="노후 건물 분포도", icon="1️⃣")
st.page_link("pages/03 노후 건물 거래 동향.py", label="노후 건물 거래 동향", icon="2️⃣")
st.page_link("pages/04 노후 건물 평당 가격.py", label="노후 건물 평당 가격", icon="3️⃣")
st.page_link("https://github.com/Kimtae00/real-estate-dashboard-team5", label="Github", icon="🚀")
