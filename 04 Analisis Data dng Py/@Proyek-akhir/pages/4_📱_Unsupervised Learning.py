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

# Setting
st.set_page_config(
    page_title="Bikeshare",
    page_icon="🚲",
)

st.markdown("<h1 style='text-align: center; color: white;'>📱 Unsupervised Learing</h1>", unsafe_allow_html=True)
st.markdown("---")

data = st.session_state["data"]
day_df = st.session_state["day_df"]

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
    Data yang akan digunakan ialah data tanpa kolom `instant` dan `dteday`, dengan peubah 
    """
)

clust_df = day_df.iloc[:, 2:]
st.dataframe(clust_df)
# Clustering
# K-Means
st.subheader('K-Means Clustering')
st.write(
    """
    > **Penentuan Jumlah *Cluster***

    Ada beberapa metode yang biasa digunakan untuk menentukan jumlah *Cluster*, salah satunya adalah metode **Elbow**.
    Pertama-tama data di *scaling* dahulu untuk setiap peubah (kolom) dengan mean 0, dan stan deviasi 1. 
    """
)
#create scaled DataFrame where each variable has mean of 0 and standard dev of 1
scaled_df = StandardScaler().fit_transform(day_df.iloc[:, -7:])

# Elbow
#initialize kmeans parameters
kmeans_kwargs = {
"init": "random",
"n_init": 10,
"random_state": 1,
}

#create list to hold SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_df)
    sse.append(kmeans.inertia_)

#visualize results
plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()
plt1 = plt.gcf()
st.pyplot(plt1)

st.caption(
    """
    Metode Elbow menetukan *cluster* dengan melihat siku mana yang paling runcing. 
    Terlihat bahwa siku yang paling runcing berada di nomor 2. 
    Sehingga jumlah cluster yang optimal menurut metode elbow adalah 2.
    """
)
st.markdown("---")

