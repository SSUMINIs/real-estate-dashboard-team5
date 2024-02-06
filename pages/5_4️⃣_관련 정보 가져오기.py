import pandas as pd
import streamlit as st

from api import get_news_data

data = pd.read_csv('data/Seoul_data.csv')

