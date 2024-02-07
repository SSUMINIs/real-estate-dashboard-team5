import streamlit as st
import numpy as np
import pydeck as pdk
import plotly as pt
import matplotlib as mtb
import geopandas as gpd
from st_pages import Page, show_pages
import pandas as pd

# Streamlit 버전 출력
st.write("Streamlit 버전:", pd.__version__)

# NumPy 버전 출력
st.write("NumPy 버전:", np.__version__)

# PyDeck 버전 출력
st.write("PyDeck 버전:", pdk.__version__)

# Plotly 버전 출력
st.write("Plotly 버전 (graph_objects):", pt.__version__)

# Matplotlib 버전 출력
st.write("Matplotlib 버전:", mtb.__version__)

# GeoPandas 버전 출력
st.write("GeoPandas 버전:", gpd.__version__)