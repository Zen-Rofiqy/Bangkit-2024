# streamlit run "1_🖥️_Main Page.py"
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
sns.set(style='dark')

st.set_page_config(
    page_title="Bikeshare",
    page_icon="🚲",
)
# Judul
st.markdown("<h2 style='text-align: center; color: white;'>Analisis <i>Pengaruh</i> Kondisi <i>Lingkungan</i> dan <i>Musim</i> Terhadap Tren <i>Penyewaan Sepeda</i>: Studi Kasus Sistem Capital Bikeshare di Washington D.C.</h2>", unsafe_allow_html=True)
st.image('https://cdn.discordapp.com/attachments/763214382020558858/1214663023310934067/fileKC_Bikes-1024x683.jpg?ex=65f9ee18&is=65e77918&hm=ab8a90a2602c0d6ce28e6c774f649f4f74b087497aed66ea00d2ea2f7824daf3&') 
st.markdown("---")
# DATA
day_df = pd.read_csv("https://raw.githubusercontent.com/Zen-Rofiqy/Bangkit-2024/main/04%20Analisis%20Data%20dng%20Py/%40Proyek-akhir/Bike-sharing-dataset/day.csv")
day_df.head(n=10)
st.session_state["day_df"] = day_df


data = pd.DataFrame(day_df)
data['season'] = data['season'].replace({1: 'M Semi', 2: 'M Panas', 3:"M Gugur", 4:"M Dingin"})
data['yr'] = data['yr'].replace({0: '2011', 1: '2012'})
data['holiday'] = data['holiday'].replace({0: 'H Kerja', 1: 'H Libur'})
data['weekday'] = data['weekday'].replace({0: 'Senin', 1: 'Selasa', 2:'Rabu', 3:'Kamis', 4:"Jum'at", 5:"Sabtu", 6:"Minggu"})
data['weathersit'] = data['weathersit'].replace({1: 'Cerah', 2: 'Berkabut', 3:'Salju Ringan', 4:'Hujan Lebat'})
data['windspeed'] = data['windspeed']*67
data['hum'] = data['hum']*100
data['temp'] = data['temp']*41
data['season']= data['season'].astype('category')
data['yr']= data['yr'].astype('category')
data['weekday']= data['weekday'].astype('category')
data['weathersit'] = data['weathersit'].astype('category')
data['dteday'] = pd.to_datetime(data['dteday'])

st.session_state["data"] = data

# Setting
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

Hari = data[(data["dteday"] >= str(start)) & (data["dteday"] <= str(end))]
Date = data[(data["dteday"] >= str(start)) & (data["dteday"] <= str(end))]
cor = data[['cnt','temp','atemp', 'hum', 'windspeed', 'casual', 'registered']]

st.session_state["Date"] = Date

# Page 1
# METADATA
st.write("## Metadata")
st.markdown("> **Latarbelakang**")
st.write(
    """
    **_Bike sharing_** atau Sistem berbagi sepeda adalah generasi baru dari **penyewaan sepeda tradisional** di mana seluruh proses mulai dari **keanggotaan**, **penyewaan**, dan **pengembalian** sepeda menjadi **otomatis**. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari posisi tertentu dan mengembalikannya di posisi lain. Saat ini, terdapat **lebih dari 500 program** berbagi sepeda di seluruh dunia yang terdiri dari **lebih dari 500k sepeda**. Saat ini, terdapat minat yang besar terhadap sistem ini karena peran penting mereka dalam masalah lalu lintas, lingkungan dan kesehatan. 

    Terlepas dari aplikasi dunia nyata yang menarik dari sistem berbagi sepeda, **karakteristik data** yang dihasilkan oleh sistem ini membuatnya menarik untuk penelitian. Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, **durasi perjalanan**, **posisi keberangkatan** dan **kedatangan secara eksplisit** dicatat dalam sistem ini. Fitur ini mengubah sistem berbagi sepeda menjadi **jaringan sensor virtual** yang dapat digunakan untuk merasakan mobilitas di kota. Dengan demikian, diharapkan sebagian besar kejadian penting di kota dapat dideteksi melalui pemantauan data ini.
    """
)
st.markdown("---")
st.markdown("> **Data set**")
st.write(
    """
    Proses penyewaan sepeda bersama sangat **berkorelasi** dengan **kondisi lingkungan** dan **musim**. Misalnya, **kondisi cuaca**, **curah hujan**, **hari dalam seminggu**, **musim**, **jam dalam sehari**, dan lain-lain dapat mempengaruhi perilaku penyewaan. Kumpulan data inti terkait dengan catatan historis selama **dua tahun** yang berkaitan dengan tahun **2011** dan **2012** dari sistem Capital Bikeshare, Washington D.C., Amerika Serikat yang tersedia untuk umum di http://capitalbikeshare.com/system-data. Kami mengumpulkan data tersebut dalam dua basis data **per jam** dan **per hari**, kemudian mengekstrak dan menambahkan **informasi cuaca** dan **musim** yang sesuai. Informasi cuaca diambil dari http://www.freemeteo.com.
    """
)
st.markdown("---")
st.markdown("> **Tugas terkait**")
st.write(
    """
    * **Regresi**:  
        **Prediksi jumlah penyewaan sepeda** per jam atau per hari **berdasarkan pengaturan lingkungan dan musim**.
        
    * **Deteksi Peristiwa dan Anomali**:  
        **Jumlah sepeda yang disewa** juga **berkorelasi** dengan beberapa **peristiwa di kota** yang dapat dengan mudah ditelusuri melalui mesin pencari.	Sebagai contoh, kueri seperti "2012-10-30 washington d.c." di Google mengembalikan hasil yang terkait dengan **Badai Sandy**. Beberapa peristiwa penting diidentifikasi dalam [1]. Oleh karena itu, data tersebut dapat digunakan untuk **validasi algoritma** **pendeteksi anomali atau kejadian**.
    """
)
st.markdown("---")
st.markdown("> **Karakteristik Dataset**")
st.write(
    """
    Baik hour.csv dan day.csv memiliki bidang berikut, kecuali hr yang tidak tersedia di day.csv
    * `instant`    : indeks catatan
    * `dteday`     : tanggal
    * `season`     : musim (1: musim semi, 2: musim panas, 3: musim gugur, 4: musim dingin)
    * `yr`         : tahun (0: 2011, 1: 2012)
    * `mnth`       : bulan (1 hingga 12)
    * `hr`         : jam (0 hingga 23)
    * `holiday`    : hari cuaca hari libur atau tidak (diambil dari http://dchr.dc.gov/page/holiday-schedule)
    * `weekday`    : hari dalam seminggu
    * `workingday` : jika hari tersebut bukan akhir pekan atau hari libur maka nilainya 1, jika tidak maka nilainya 0.
    * `weathersit` : 
        - 1: Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian
        - 2: Kabut + Mendung, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
        - 3: Salju Ringan, Hujan Ringan + Badai Petir + Awan berserakan, Hujan Ringan + Awan berserakan
        - 4: Hujan Lebat + Hujan Es + Badai Petir + Kabut, Salju + Kabut
    * `temp`       : Suhu yang dinormalisasi dalam Celcius. Nilai dibagi menjadi 41 (maks)
    * `atemp`      : Suhu perasaan yang dinormalisasi dalam Celcius. Nilai dibagi menjadi 50 (maks)
    * `hum`        : Kelembapan yang dinormalisasi. Nilai dibagi menjadi 100 (maks)
    * `windspeed`  : Kecepatan angin yang dinormalisasi. Nilai dibagi menjadi 67 (maks)
    * `casual`     : jumlah pengguna biasa
    * `registered` : jumlah pengguna terdaftar
    * `cnt`        : jumlah total sepeda yang disewa termasuk yang kasual dan terdaftar
    """
)
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: white;'>Tabel Data</h2>", unsafe_allow_html=True)
st.dataframe(Hari)