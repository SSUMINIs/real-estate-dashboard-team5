import streamlit as st
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import geopandas as gpd
from st_pages import Page, show_pages

# Streamlit 버전 출력
st.write("Streamlit 버전:", st.__version__)

# NumPy 버전 출력
st.write("NumPy 버전:", np.__version__)

# PyDeck 버전 출력
st.write("PyDeck 버전:", pdk.__version__)

# Plotly 버전 출력
st.write("Plotly 버전 (graph_objects):", go.__version__)
st.write("Plotly 버전 (express):", px.__version__)

# Matplotlib 버전 출력
st.write("Matplotlib 버전:", plt.__version__)

# GeoPandas 버전 출력
st.write("GeoPandas 버전:", gpd.__version__)

st.set_page_config(page_title="🏢 Real Estate Project Team5️⃣",layout="wide")

# Page("app.py", "🏢 Real Estate Project Team5️⃣")
# Optional -- adds the title and icon to the current page

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Page("app.py", "🏢 Real Estate Project Team5️⃣"),
        Page("pages/1️⃣_노후 건물 분포도.py", "노후 건물 분포도", "1️⃣"),
        Page("pages/2️⃣_노후 건물 거래 동향.py", "노후 건물 거래 동향", "2️⃣"),
        Page("pages/3️⃣_노후 건물 평당 가격.py", "노후 건물 평당 가격", "3️⃣"),
        Page("pages/4️⃣_관련 기사 가져오기.py", "관련 기사 가져오기", "4️⃣")
    ]
)

st.header('Readme 작성 !')

st.sidebar.markdown("""
    <a href="https://github.com/Kimtae00/real-estate-dashboard-team5">
        <img src="https://simpleicons.org/icons/github.svg" width="25" height="25" />
    </a>
""", unsafe_allow_html=True)
