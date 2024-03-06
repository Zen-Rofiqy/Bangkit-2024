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
from scipy import stats
import sys
import io
from babel.numbers import format_currency
import matplotlib.dates as mdates
from PIL import Image

# Setting
st.set_page_config(
    page_title="Bikeshare",
    page_icon="🚲",
)

st.markdown("<h1 style='text-align: center; color: white;'>🛠️ Data Wrangling</h1>", unsafe_allow_html=True)
st.markdown("---")

data = st.session_state["data"]

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

# Data Wrangling
st.subheader("Assessing Data")
st.caption(
    """
    Sebagai permulaan, kita memeriksa tipe data data dari tiap kolom yang terdapat dalam `data`. Proses ini dapat dilakukan menggunakan method `data.info()`.
    """
)
st.markdown('`print(data.info())`')
st.text(
    """
    ---------------------------------------------
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 731 entries, 0 to 730
    Data columns (total 16 columns):
    #   Column      Non-Null Count  Dtype         
    ---  ------      --------------  -----         
    0   instant     731 non-null    int64         
    1   dteday      731 non-null    datetime64[ns]
    2   season      731 non-null    category      
    3   yr          731 non-null    category      
    4   mnth        731 non-null    int64         
    5   holiday     731 non-null    object        
    6   weekday     731 non-null    category      
    7   workingday  731 non-null    int64         
    8   weathersit  731 non-null    category      
    9   temp        731 non-null    float64       
    10  atemp       731 non-null    float64       
    11  hum         731 non-null    float64       
    12  windspeed   731 non-null    float64       
    13  casual      731 non-null    int64         
    14  registered  731 non-null    int64         
    15  cnt         731 non-null    int64         
    dtypes: category(4), datetime64[ns](1), float64(4), int64(6), object(1)
    memory usage: 72.3+ KB
    """
)
st.caption(
    """
    Jika diperhatikan, tidak ada masalah dengan tipe data dari seluruh kolom tersebut. Juga tidak ada perbedaan pada jumlah data pada kolom gender. Hal ini menunjukkan tidak adanya missing values pada semua kolom atau peubah.
    """
)

col1, col2= st.columns(2)
with col1 : 
    st.markdown(""" Tipe Data """)  
    st.dataframe(data.dtypes)
    st.caption("Terdapat 4 tipe data beruba, yakni kategorik, numerik (rasio dan interval), dan date.")
with col2 :
    st.markdown(""" Data NA""")
    st.dataframe(data.isnull().sum())
    st.caption("Memang terbukti bahwa tidak ada missing value pada `data`.")
st.write("Jumlah data duplikat: " + str(data.duplicated().sum()))
st.caption("Tidak ada Data yang Duplikat")
st.markdown("---")

st. subheader("Cleaning Data")
st.markdown(""" Data setelah di cleaning""")
st.dataframe(data)
st.caption("Karena tidak ada masalah apapun, maka tidak perlu dilakukan penanganan apapun.")