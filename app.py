import streamlit as st
from st_pages import Page, show_pages


st.set_page_config(page_title="🏢 Real Estate Project Team5️⃣",layout="wide")

# Page("app.py", "🏢 Real Estate Project Team5️⃣")
# Optional -- adds the title and icon to the current page

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Page("app.py", "🏢 Real Estate Project Team5️⃣"),
        Page("pages/1_1️⃣_노후 건물 분포도.py", "노후 건물 분포도", "1️⃣"),
        Page("pages/2_2️⃣_노후 건물 거래 동향.py", "노후 건물 거래 동향", "2️⃣"),
        Page("pages/3_3️⃣_노후 건물 평당 가격.py", "노후 건물 평당 가격", "3️⃣"),
        Page("pages/4_4️⃣_관련 기사 가져오기.py", "관련 기사 가져오기", "4️⃣")
    ]
)

st.header('Welcome Our Project 👋')

st.title("real-estate-dashboard 프로젝트 소개")
st.markdown("본 프로젝트는 서울시의 2022년과 2023년 부동산 거래 데이터와 법정동 좌표를 활용하여 재개발이 예상되는 지역을 식별하고, Naver Open Search API를 활용하여 관련된 뉴스 기사를 수집하여 예측 결과를 예측 결과를 더 깊이 분석할 수 있도록 구현해보았습니다.")
st.markdown("---")

st.markdown("## 팀원 소개")
st.markdown("1. [hyelin606](https://github.com/hyelin606)")
st.markdown("2. [jianteow](https://github.com/jianteow)")
st.markdown("3. [JiHoonYoon00](https://github.com/JiHoonYoon00)")
st.markdown("4. [SSUMINIs](https://github.com/SSUMINIs)")
st.markdown("---")

st.markdown("## 데이터셋 출처")
st.markdown("- [서울시 부동산 실거래가 정보](https://data.seoul.go.kr/dataList/OA-21275/S/1/datasetView.do)")
st.markdown("- [전국 법정동 좌표](https://herjh0405.tistory.com/156)")
st.markdown("- [SVG 지리정보](http://www.gisdeveloper.co.kr/?p=2332)")
st.markdown("---")

st.markdown("## Seoul_data.csv 주요 칼럼")
st.markdown("- ACC_YEAR : 접수년도")
st.markdown("- SSG_CD : 자치구코드")
st.markdown("- SGG_NM : 자치구명")
st.markdown("- BJDONG_CD : 법정동코드")
st.markdown("- BJDONG_CD : 법정동명")
st.markdown("- BLDG_NM : 건물명")
st.markdown("- DEAL_YMD : 계약일")
st.markdown("- OBJ_AMT : 물건금액")
st.markdown("- BLDG_AREA : 건물면적 (m²)")
st.markdown("- BUILD_YEAR : 건축년도")
st.markdown("- HOUSE_TYPE : 건물용도")
st.markdown("- CENTER_LONG : 법정동 기준 경도")
st.markdown("- CENTER_LATI : 법정동 기준 위도")
st.markdown("- PRICE_PER : 평당 가격 (만원)")

st.markdown("---")

st.markdown("## 구조")
st.code('''
├── .devcontainer # 개발 환경 컨테이너 설정
├── .gitignore # Git에서 추적하지 않을 파일 목록 
├── .venv # 가상 환경 설정
│ 
├── data # 데이터 분석에 사용되는 데이터셋 폴더
│ ├── 단독다가구.csv # 법정동별 평균 평당가격이 포함된 건물유형(HOUSE_TYPE)이 '단독다가구'인 데이터
│ ├── 아파트.csv # 법정동별 평균 평당가격이 포함된 건물유형(HOUSE_TYPE)이 '아파트'인 데이터
│ ├── 연립다세대.csv # 법정동별 평균 평당가격이 포함된 건물유형(HOUSE_TYPE)이 '연립다세대'인 데이터
│ ├── 오피스텔.csv # 법정동별 평균 평당가격이 포함된 건물유형(HOUSE_TYPE)이 '오피스텔'인 데이터
│ ├── Seoul_data.csv # 서울시 부동산 실거래 데이터(2022, 2023년)
│ ├── seoul_sig_cd.geojson # 서울시 구역별 지도 데이터
│ └── seoul.geojson # 서울시 지리 데이터
│ 
├── images # 분석에 사용되는 이미지
│ ├── 재개발 선정 지역.png
│ 
├── pages # 스트림릿 페이지 파일
│ ├── 1_1️⃣_노후 건물 분포도.py # 노후 건물 분포도 페이지
│ ├── 2_2️⃣_노후 건물 거래 동향.py # 노후 건물 거래 동향 페이지
│ ├── 3_3️⃣_노후 건물 평당 가격.py # 노후 건물 평당 가격 페이지
│ ├── 4_4️⃣_관련 정보 가져오기.py # 재개발 부지로 선정된 지역의 재개발 관련 뉴스 정보를 가져오는 페이지
│ 
├── app.py # 스트림릿 앱 실행 파일
├── crawling.py # 크롤링 함수가 정의된 파일
│ 
├── requirements.txt # 필요한 파이썬 패키지 목록
└── README.md # 프로젝트 설명 파일
''')

st.markdown("---")

st.markdown("## 기술 스택")
st.markdown("- **Streamlit** : 배포 및 대시보드 개발")
st.markdown("- **Naver Open Search API** : 네이버 뉴스 정보 크롤링")
st.markdown("- **QGIS** : 지리정보 활용 (v3.34.3)")

st.markdown("---")

st.markdown("## 라이브러리 소개(requirements.txt)")
st.markdown("##### 대시보드 개발")
st.markdown("- **streamlit==1.31.0**")
st.markdown("##### 데이터 전처리")
st.markdown("- **pandas==2.2.0**")
st.markdown("- **numpy==1.26.3**")
st.markdown("##### 시각화")
st.markdown("- **matplotlib==3.8.2**")
st.markdown("- **plotly==5.18.0**")
st.markdown("- **pydeck==0.8.1b**")
st.markdown("- **geopandas==0.14.3**")
st.markdown("##### 크롤링 환경변수 설정")
st.markdown("- **python-dotenv==1.0.1**")
st.markdown("##### streamlit 페이지 처리")
st.markdown("- **st_pages**")

st.markdown("---")

st.markdown("## 서비스 다이어그램")
st.markdown("아래는 서비스 아키텍처를 보여주는 다이어그램입니다.")
st.image("./서비스 다이어그램.png", use_column_width=True)

st.markdown("---")

st.markdown("## Naver Open Search API")
st.markdown("아래는 Open Search API가 호출되는 로직입니다.")
st.image("./서비스 다이어그램.png", use_column_width=True)

st.markdown("---")

st.markdown('<p align="center"><img src="https://img.shields.io/badge/language-python-blue?style"/> <img src="https://img.shields.io/badge/library-streamlit-red?style"/> <img src="https://img.shields.io/github/license/maxam2017/productive-box"/></p>', unsafe_allow_html=True)

# 깃허브 레포지토리 주소
st.sidebar.title("Github")
st.sidebar.markdown("""
    <a href="https://github.com/Kimtae00/real-estate-dashboard-team5">
        <img src="https://simpleicons.org/icons/github.svg" width="40" height="40" />
    </a>
""", unsafe_allow_html=True)