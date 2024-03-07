# IMPORT
import numpy as np
import pandas as pd
import scipy
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy as sqla
import streamlit as st
import time
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy import stats
import sys
import io
from babel.numbers import format_currency
import matplotlib.dates as mdates
from PIL import Image
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

# Setting
st.set_page_config(
    page_title="Bikeshare",
    page_icon="🚲",
)

st.markdown("<h1 style='text-align: center; color: white;'>📈 Supervised Learning</h1>", unsafe_allow_html=True)
st.markdown("---")

data = st.session_state["data"]
day_df = st.session_state["day_df"]
dw_df = st.session_state["dw_df"]

min_date = data["dteday"].min()
max_date = data["dteday"].max()

def count(dates) :
    sumcount = dates['cnt'].sum()
    return sumcount

# Sidebar
st.sidebar.success("Select a page above.")
with st.sidebar:       
    start, end = st.date_input(
        label='Tanggal',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Data
st.write(
    """
    Data yang akan digunakan ialah data tanpa kolom `instant` dan `dteday`, serperti tabel berikut.
    """
)

st.dataframe(dw_df.drop(['dteday', 'instant'], axis=1))
st.caption(
    """
    Terlihat bahwa ada beberapa data yang kategorik, jadi Data akan dibuat dummy variable dulu
    sebelum dilakukan *clustering*.
    """
)

#Dummy
dw_dummy = pd.get_dummies(dw_df.drop(['dteday', 'instant'], axis=1), drop_first=True)

with st.expander("Hasil Dummy Variable"):
    st.dataframe(dw_dummy)  

