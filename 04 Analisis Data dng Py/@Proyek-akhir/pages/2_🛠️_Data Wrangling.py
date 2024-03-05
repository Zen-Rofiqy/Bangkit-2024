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
        label='Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Data Wrangling
st.subheader("Assessing Data")
col1, col2= st.columns(2)
with col1 : 
    st.markdown(""" Type Data """)
    st.caption(
        """
        Sebagai permulaan, kita memeriksa tipe data data dari tiap kolom yang terdapat dalam `data`. Proses ini dapat dilakukan menggunakan method `.dtypes`.
        """
    )
    st.dataframe(data.dtypes)
with col2 :
    st.markdown(""" Data NA""")
    st.dataframe(data.isnull().sum())
st.write("Jumlah data duplikat: " + str(data.duplicated().sum()))
st. subheader("Cleaning Data")
st.markdown(""" Data setelah di cleaning""")
st.dataframe(data)