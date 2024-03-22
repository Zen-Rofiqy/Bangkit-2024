# streamlit run coba2.py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency
import matplotlib.dates as mdates
sns.set(style='dark')

############################
day = pd.read_csv("https://raw.githubusercontent.com/rafi2411/Bangkit-2024/main/Streamlit/day.csv")
day.head()

days = day
days['season']=days['season'].replace((1,2,3,4), ('spring','summer', 'autumn', 'winter'))
days['yr']=days['yr'].replace((0,1), (2011, 2012))
days['weekday']=days['weekday'].replace((0,1,2,3,4,5,6), ('Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu'))
days['weathersit']=days['weathersit'].replace((1,2,3,4), ('Clear','Mist', 'Rain', 'Storm'))
days['windspeed'] = days['windspeed']*67
days['hum'] = days['hum']*100
days['temp'] = days['temp']*41
days['season']=days['season'].astype('category')
days['yr']=days['yr'].astype('category')
days['weekday']=days['weekday'].astype('category')
days['weathersit']=days['weathersit'].astype('category')
days['dteday'] = pd.to_datetime(days['dteday'])
#############################

try:
    min_date = days["dteday"].min()
    max_date = days["dteday"].max()

    def count(dates) :
        sumcount = dates['cnt'].sum()
        return sumcount

    # Sidebar
    with st.sidebar:
        # Menambahkan logo perusahaan
        st.image("https://github.com/rafi2411/Bangkit-2024/blob/main/Streamlit/Logo.png?raw=true")
        
        start, end = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    Hari = day[(day["dteday"] >= str(start)) & (day["dteday"] <= str(end))]
    Date = days[(days["dteday"] >= str(start)) & (days["dteday"] <= str(end))]
    cor = days[['cnt','temp','atemp', 'hum', 'windspeed', 'casual', 'registered']]
    
    page = st.sidebar.selectbox('Menu Utama', ('Data','Data Wrangling', 'Eksplorasi', 'Analisis'))

    # Konten untuk Halaman 1
    if page == 'Data':
        st.markdown("<h1 style='text-align: center; color: white;'>------Data------</h1>", unsafe_allow_html=True)
        st.dataframe(Hari)
        st.write("Data yang digunakan berasal dari file day.csv. terdiri dari 16 kolom, dengan keterangan sebagai berikut.")
        st.markdown("""
        - instant : record index
        - dteday : date
        - season : season
        - yr : year
        - mnth : month ( 1 to 12)
        - holiday : weather day is holiday or not
        - weekday : day of the week
        - workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
        - weathersit : clear, mist, rain, storm
        - temp : Normalized temperature in Celsius
        - atemp: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
        - hum: Normalized humidity
        - windspeed: Normalized wind speed
        - casual: count of casual users
        - registered: count of registered users
        - cnt: count of total rental bikes including both casual and registered
        
        """)
        
    # Konten untuk Halaman 2
    elif page == 'Data Wrangling':
        st.subheader("Assessing Data")
        col1, col2= st.columns(2)
        with col1 : 
            st.markdown(""" Type Data """)
            st.dataframe(day.dtypes)
        with col2 :
            st.markdown(""" Data NA""")
            st.dataframe(day.isnull().sum())
        st.write("Jumlah data duplikat: " + str(day.duplicated().sum()))
        st. subheader("Cleaning Data")
        st.markdown(""" Data setelah di cleaning""")
        st.dataframe(days)
        
    elif page == 'Eksplorasi':
        st.markdown("<h1 style='text-align: center; color: white;'>----Eksplorasi----</h1>", unsafe_allow_html=True)
        st.subheader('Jumlah Pengunjung')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("  Total Rents", value=count(Date))
        with col2:
            st.metric("  Total Membered", value=Date['registered'].sum())
        with col3:
            st.metric("  Total Regular", value=Date['casual'].sum())
        
        st.subheader("Korelasi")
        st.write(cor.corr())

        # Membuat grafik dengan Seaborn
        st.subheader("Plot Dinamis")
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.lineplot(x='dteday', y='cnt', data=Date, color="steelblue") 
        ax.set_title("Pola Penyewa Harian", size=25)
        ax.set_ylabel("Jumlah")
        ax.set_xlabel("Tanggal")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        st.pyplot(fig)
        st.write("*Sesuaikan menurut rentang waktu")
        st.markdown("""Terjadi penurunan jumlah penyewa dari bulan Oktober 2012 hingga awal tahun 2013""")
        
        #Plot Bersifat Statis        
        #Histogram
        st.subheader("Plot Statis")
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.histplot(days['cnt'], kde=True)
        ax.set_title("Sebaran penyewa pada Tahun 2011-2012", size=25)
        ax.set_ylabel("Frekuensi")
        ax.set_xlabel("Jumlah penyewa")
        st.pyplot(fig)
        if st.button("Interpretasi 1"):   
            st.write("Bentuk sebaran dari pola penyewa harian menunjukkan bentuk yang cenderung simetris berarti nilai dari mean, modus, dan mediannya cenderung sama")
        
        col1, col2 = st.columns(2)
        with col1:
            #tahun
            fig, ax = plt.subplots(figsize=(35, 30))
            years = days.groupby(by = "yr").agg({
                'cnt':'sum'
                })
            years['cnt'] = years['cnt']/1000

            sns.barplot(x='yr', y='cnt', data=years, color="#AAD7D9")
            ax.set_title("Jumlah Penyewa Berdasarkan Tahun", size=80)
            ax.set_ylabel("Penyewa (per satuan ribu)",fontsize=50)
            ax.set_xlabel("Tahun",fontsize=50)
            ax.tick_params(axis='y', labelsize=35)
            ax.tick_params(axis='x', labelsize=50)
            nilai_tertinggi = years['cnt'].max()
            # Cari batang yang memiliki nilai tertinggi
            for bar in ax.patches:
                if bar.get_height() == nilai_tertinggi:
                    bar.set_color('#92C7CF')
            st.pyplot(fig)
            
        with col2:
            fig, ax = plt.subplots(figsize=(35, 30))
            weathersit = days.groupby(by = "weathersit").agg({
                'cnt':'sum'
                })
            weathersit['cnt'] = weathersit['cnt']/1000

            sns.barplot(x='weathersit', y='cnt', data=weathersit, color="#AAD7D9")
            ax.set_title("Jumlah Penyewa Berdasarkan Cuaca", size=80)
            ax.set_ylabel("Penyewa (per satuan ribu)",fontsize=50)
            ax.set_xlabel("Cuaca",fontsize=50)
            ax.tick_params(axis='y', labelsize=35)
            ax.tick_params(axis='x', labelsize=50)
            nilai_tertinggi = weathersit['cnt'].max()
            # Cari batang yang memiliki nilai tertinggi
            for bar in ax.patches:
                if bar.get_height() == nilai_tertinggi:
                    bar.set_color('#92C7CF')
            st.pyplot(fig)
        if st.button("Interpretasi 2"):   
            st.write("Berdasarkan pengamatan melalui kedua plot, didapati bahwa terjadi peningkatan jumlah pengunjung dari tahun 2011 sampai tahun 2012. Kemudian apabila diamati pada barplot cuaca, terdapat perbedaan yang signifikan diantara setiap kategori cuaca. Jadi jenis cuaca sangat berpengaruh terhadap jumlah Penyewa")
       
        col1, col2 = st.columns(2)
        with col1:
            # weekday
            fig, ax = plt.subplots(figsize=(35, 30))
            weekday = days.groupby(by = "weekday").agg({
                'cnt':'sum'
                })
            weekday['cnt'] = weekday['cnt']/1000
            index = [6,5,3,1,0,4,2]
            weekday = weekday.iloc[index]

            sns.barplot(x='weekday', y='cnt', data=weekday, color="#AAD7D9")
            ax.set_title("Jumlah Penyewa Berdasarkan Hari", size=80)
            ax.set_ylabel("Penyewa (per satuan ribu)",fontsize=50)
            ax.set_xlabel("Hari",fontsize=50)
            ax.tick_params(axis='y', labelsize=35)
            ax.tick_params(axis='x', labelsize=50)
            nilai_tertinggi = weekday['cnt'].max()
            # Cari batang yang memiliki nilai tertinggi
            for bar in ax.patches:
                if bar.get_height() == nilai_tertinggi:
                    bar.set_color('#92C7CF')
            st.pyplot(fig)
        with col2:
            
            # Musim
            fig, ax = plt.subplots(figsize=(35, 30))
            sea = days.groupby(by = "season").agg({
                'cnt':'sum'
                })
            sea['cnt'] = sea['cnt']/1000
            sea = sea.sort_values(by='season', ascending=False)
            index = [2,1,3,0]
            sea = sea.iloc[index]

            sns.barplot(x='season', y='cnt', data=sea, color="#AAD7D9")
            ax.set_title("Jumlah Penyewa Berdasarkan Musim", size=80)
            ax.set_ylabel("Penyewa (per satuan ribu)",fontsize=50)
            ax.set_xlabel("Musim",fontsize=50)
            ax.tick_params(axis='y', labelsize=35)
            ax.tick_params(axis='x', labelsize=50)
            nilai_tertinggi = sea['cnt'].max()
            # Cari batang yang memiliki nilai tertinggi
            for bar in ax.patches:
                if bar.get_height() == nilai_tertinggi:
                    bar.set_color('#92C7CF')
            st.pyplot(fig)
        if st.button("Interpretasi 3"):
            st.write("Berdasarkan barplot harian, tidak terdapat perbedaan yang jelas diantara jenis hari terhadap jumlah penyewa yang datang. Namun, jika diamati lebih detil, hari Jumat dan Sabtu memiliki jumlah penyewa paling tinggi diantara hari lainnya. Hal ini bisa terjadi karena pada hari tersebut terdapat hari libur atau weekend di hari besoknya. Kemudian, jika diamati pada barplot musim, didapat bahwa jumlah penyewa paling banyak terdapat pada musim gugur.")
        
        # Suhu
        cor1 = days['temp'].corr(days['cnt'])
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.regplot(x='temp', y='cnt', data=days, line_kws={'color': '#A25772'}, scatter_kws={'color': '#9EB8D9'})
        ax.set_title("Pengaruh Suhu terhadap Jumlah Penyewa", size = 20)
        ax.set_ylabel("Jumlah", size= 15)
        ax.set_xlabel("Suhu (Celsius)", size=15)
        st.text(f"Korelasi: {cor1:.2f}")
        st.pyplot(fig)
        if st.button("Interpretasi"):
            st.write("Berdasarkan plot regresi, terdapat hubungan linier positif yang cenderung kuat diantara peubah suhu dan jumlah penyewa. Oleh karena itu, semakin tinggi suhu maka semakin tinggi jumlah penyewa pada selang suhu=(0,36)")
       
        # humidity
        cor2 = days['hum'].corr(days['cnt'])
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.regplot(x='hum', y='cnt', data=days, line_kws={'color': '#A25772'}, scatter_kws={'color': '#9EB8D9'})
        ax.set_title("Pengaruh Kelembapan terhadap Jumlah Penyewa")
        ax.set_ylabel("Jumlah")
        ax.set_xlabel("Kelembapan")
        st.text(f"Korelasi: {cor2:.2f}")
        st.pyplot(fig)
        if st.button("Interpretasi 4"):
            st.write("Berdasarkan plot regresi, terdapat hubungan linier negatif yang sangat lemah bahkan cenderung tidak ada diantara peubah kelembapan dan jumlah penyewa. Oleh karena itu, tidak terdapat perubahan yang signifikan atas perubahan kelembapan pada selang kelembapan=(0,100)")
        
        # windspeed
        cor3 = days['windspeed'].corr(days['cnt'])
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.regplot(x='windspeed', y='cnt', data=days, line_kws={'color': '#A25772'}, scatter_kws={'color': '#9EB8D9'})
        ax.set_title("Pengaruh Kecepatan Angin terhadap Jumlah Penyewa")
        ax.set_label("Jumlah")
        ax.set_xlabel("Kecepatan Angin")
        st.text(f"Korelasi: {cor3:.2f}")
        st.pyplot(fig)
        if st.button("Interpretasi 5"):
            st.write("Berdasarkan plot regresi, terdapat hubungan linier negatif yang lemah diantara peubah kecepatan udara dan jumlah penyewa. Oleh karena itu, tidak terdapat perubahan yang signifikan atas perubahan kecepatan angin pada selang kecepatan angin=(0,35)")
    
    #Konten Untuk Halaman 3 
    elif page == 'Analisis':
        st.markdown("<h1 style='text-align: center; color: white;'>----Analisis----</h1>", unsafe_allow_html=True)
        st.subheader("PCA")
        st.markdown(""" Melakukan analisis cluster dengan PCA untuk mengetahui pengelompokkan dataframe ketika dimensinya direduksi menjadi 2 """)
        kmeans = KMeans(n_clusters=5)

        # Melakukan clustering pada data
        kmeans.fit(cor)

        # Menambahkan kolom label klaster ke DataFrame
        cor['cluster'] = kmeans.labels_
        pca = PCA(n_components=2)
        data_reduced = pca.fit_transform(cor)
        # Visualisasi cluster menggunakan scatter plot pada ruang yang direduksi
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.scatterplot(x=data_reduced[:, 0], y=data_reduced[:, 1], hue=cor['cluster'], palette='viridis')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_title('Clustering Result (PCA)')
        st.pyplot(fig)
        st.markdown("Setelah dilakukan visualisasi dengan 5 pengelompokkan didapat pembagian kelompok yang cukup jelas dan dibatasi dengan berbagai warna.")
                     
except Exception as e:
    st.error(f"Terjadi kesalahan: Masukkan tanggal dengan benar{e}")