import streamlit as st

st.set_page_config(
  layout="wide",  # 더 많은 공간을 위한 넓은 레이아웃 설정
)

# # 아이콘을 포함한 페이지 링크 생성
# st.page_link("pages/1_👋_Hi There.py", label="Hi There", icon="👋")
# st.page_link("pages/2_1️⃣_노후 건물 분포도.py", label="노후 건물 분포도", icon="1️⃣")
# st.page_link("pages/3_2️⃣_노후 건물 거래 동향.py", label="노후 건물 거래 동향", icon="2️⃣")
# st.page_link("pages/4_3️⃣_노후 건물 평당 가격.py", label="노후 건물 평당 가격", icon="3️⃣")
# st.page_link("https://github.com/Kimtae00/real-estate-dashboard-team5", label="Github", icon="🚀")

from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Page("app.py", "real estate project team5", "🏢"),
        Page("pages/1_👋_Hi There.py", "Hi There"),
        Page("pages/2_1️⃣_노후 건물 분포도.py", "노후 건물 분포도", "1️⃣"),
        Page("pages/3_2️⃣_노후 건물 거래 동향.py", "노후 건물 거래 동향", "2️⃣"),
        Page("pages/4_3️⃣_노후 건물 평당 가격.py", "노후 건물 평당 가격", "3️⃣"),
    ]
)

st.header('Readme 작성 !')

st.sidebar.markdown("""
    <a href="https://github.com/Kimtae00/real-estate-dashboard-team5">
        <img src="https://simpleicons.org/icons/github.svg" width="25" height="25" />
    </a>
""", unsafe_allow_html=True)
