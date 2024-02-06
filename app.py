import streamlit as st

st.set_page_config(page_title="🏢 Real Estate Project Team5️⃣",layout="wide")

from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
# add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Page("app.py", "🏢 Real Estate Project Team5️⃣"),
        Page("pages/1_👋_Hi There.py", "Hi There", "👋"),
        Page("pages/2_1️⃣_노후 건물 분포도.py", "노후 건물 분포도", "1️⃣"),
        Page("pages/3_2️⃣_노후 건물 거래 동향.py", "노후 건물 거래 동향", "2️⃣"),
        Page("pages/4_3️⃣_노후 건물 평당 가격.py", "노후 건물 평당 가격", "3️⃣"),
        Page("pages/5_4️⃣_관련 정보 가져오기.py", "관련 기사 가져오기", "4️⃣")
    ]
)

st.header('Readme 작성 !')

st.sidebar.markdown("""
    <a href="https://github.com/Kimtae00/real-estate-dashboard-team5">
        <img src="https://simpleicons.org/icons/github.svg" width="25" height="25" />
    </a>
""", unsafe_allow_html=True)
