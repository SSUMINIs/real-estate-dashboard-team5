import streamlit as st

st.set_page_config(
  layout="wide",  
)

# 아이콘을 포함한 페이지 링크 생성
st.page_link("pages/1_👋_Hi There.py", label="Hi There", icon="👋")
st.page_link("pages/2_1️⃣_노후 건물 분포도.py", label="노후 건물 분포도", icon="1️⃣")
st.page_link("pages/3_2️⃣_노후 건물 거래 동향.py", label="노후 건물 거래 동향", icon="2️⃣")
st.page_link("pages/4_3️⃣_노후 건물 평당 가격.py", label="노후 건물 평당 가격", icon="3️⃣")
st.page_link("pages/5_4️⃣_관련 정보 가져오기.py", label="관련 기사 가져오기", icon="4️⃣")
st.page_link("https://github.com/Kimtae00/real-estate-dashboard-team5?tab=readme-ov-file", label="Github", icon="🚀")

st.header('Readme 작성 !')

st.sidebar.markdown("""
    <a href="https://github.com/Kimtae00/real-estate-dashboard-team5">
        <img src="https://simpleicons.org/icons/github.svg" width="25" height="25" />
    </a>
""", unsafe_allow_html=True)
