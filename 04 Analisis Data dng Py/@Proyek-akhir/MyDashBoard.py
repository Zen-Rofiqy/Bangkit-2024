# streamlit run MyDashBoard.py
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
from IPython.display import display, Image
from babel.numbers import format_currency
import matplotlib.dates as mdates
from PIL import Image
sns.set(style='dark')

# DATA
day_df = pd.read_csv("https://raw.githubusercontent.com/Zen-Rofiqy/Bangkit-2024/main/04%20Analisis%20Data%20dng%20Py/%40Proyek-akhir/Bike-sharing-dataset/day.csv")
day_df.head(n=10)

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

try:
    min_date = data["dteday"].min()
    max_date = data["dteday"].max()

    def count(dates) :
        sumcount = dates['cnt'].sum()
        return sumcount

    # Sidebar
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
    
    page = st.sidebar.selectbox('Menu Utama', ('Data', 'Data Wrangling', 'Eksplorasi'))

    # Page 1
    if page == 'Data':
        # METADATA
        st.write("## Metadata")
        st.markdown("> Latarbelakang")
        st.write(
            """
            **_Bike sharing_** atau Sistem berbagi sepeda adalah generasi baru dari **penyewaan sepeda tradisional** di mana seluruh proses mulai dari **keanggotaan**, **penyewaan**, dan **pengembalian** sepeda menjadi **otomatis**. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari posisi tertentu dan mengembalikannya di posisi lain. Saat ini, terdapat **lebih dari 500 program** berbagi sepeda di seluruh dunia yang terdiri dari **lebih dari 500k sepeda**. Saat ini, terdapat minat yang besar terhadap sistem ini karena peran penting mereka dalam masalah lalu lintas, lingkungan dan kesehatan. 

            Terlepas dari aplikasi dunia nyata yang menarik dari sistem berbagi sepeda, **karakteristik data** yang dihasilkan oleh sistem ini membuatnya menarik untuk penelitian. Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, **durasi perjalanan**, **posisi keberangkatan** dan **kedatangan secara eksplisit** dicatat dalam sistem ini. Fitur ini mengubah sistem berbagi sepeda menjadi **jaringan sensor virtual** yang dapat digunakan untuk merasakan mobilitas di kota. Dengan demikian, diharapkan sebagian besar kejadian penting di kota dapat dideteksi melalui pemantauan data ini.
            """
        )
        st.markdown("> Data set")
        st.write(
            """
            Proses penyewaan sepeda bersama sangat **berkorelasi** dengan **kondisi lingkungan** dan **musim**. Misalnya, **kondisi cuaca**, **curah hujan**, **hari dalam seminggu**, **musim**, **jam dalam sehari**, dan lain-lain dapat mempengaruhi perilaku penyewaan. Kumpulan data inti terkait dengan catatan historis selama **dua tahun** yang berkaitan dengan tahun **2011** dan **2012** dari sistem Capital Bikeshare, Washington D.C., Amerika Serikat yang tersedia untuk umum di http://capitalbikeshare.com/system-data. Kami mengumpulkan data tersebut dalam dua basis data **per jam** dan **per hari**, kemudian mengekstrak dan menambahkan **informasi cuaca** dan **musim** yang sesuai. Informasi cuaca diambil dari http://www.freemeteo.com.
            """
        )
        st.markdown("> Karakteristik Dataset")
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
        st.markdown("<h1 style='text-align: center; color: white;'>Tabel Data</h1>", unsafe_allow_html=True)
        st.dataframe(Hari)

    # Page 2
    elif page == 'Data Wrangling':
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

    # Page3
    elif page == 'Eksplorasi':
        # EKSPLORASI
        st.markdown("<h1 style='text-align: center; color: white;'>Eksplorasi Data</h1>", unsafe_allow_html=True)
        st.subheader('Jumlah Total')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("  Total Rents", value=count(Date))
        with col2:
            st.metric("  Total Membered", value=Date['registered'].sum())
        with col3:
            st.metric("  Total Regular", value=Date['casual'].sum())
        
        # Sebaran Disktrit
        st.write("\n\n")
        st.subheader('Sebaran Diskrit')
        def plot_disk(data_frame, column, names=None):
            # Mendapatkan kategori unik dan warna untuk plot
            max_value = data_frame[column].value_counts().idxmax()
            categories = data_frame[column].unique()
            colors = ['#1380A1' if x == max_value else '#dddddd' for x in categories]

            # Mendapatkan nama kategori
            category_names = [str(cat) for cat in categories]
            if names:
                category_names = names

            # Membuat countplot
            plt.figure(figsize=(10, 6))
            sns.countplot(x=column, data=data_frame, order=categories, palette=colors)
            plt.title(f'Sebaran {column}')
            plt.xlabel(f'\n{column}')
            plt.ylabel('Banyaknya Hari')

            # Mengatur label pada sumbu x
            plt.xticks(ticks=range(len(categories)), labels=category_names)

            # Menyimpan plot dalam variabel
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Menutup plot untuk plot selanjutnya
            plt.close()

            return buffer

        # Menyimpan plot 
        c_season = plot_disk(day_df, 'season', names=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
        c_holiday = plot_disk(day_df, 'holiday', names=['Hari Kerja', 'Hari Libur'])
        c_weathersit = plot_disk(day_df, 'weathersit', names=['Cerah', 'Berkabut', 'Salju Ringan'])
        
        # Menampilkan plot
        c1, c2, c3 = st.columns((1,1,1))
        c1.markdown("**Sebaran Musim**")
        c1.image(Image.open(io.BytesIO(c_season.getvalue())), caption='Caption')

        c2.markdown("**Sebaran Hari Libur**")
        c2.image(Image.open(io.BytesIO(c_holiday.getvalue())), caption='Caption')

        c3.markdown("**Sebaran Cuaca**")
        c3.image(Image.open(io.BytesIO(c_weathersit.getvalue())), caption='Caption')
        # ------

        # Sebaran Kontinu
        st.write("\n\n")
        st.subheader('Sebaran Kontinu')
        def plot_kon(data_frame, column):
            # Membuat subplots
            fig, ax = plt.subplots(figsize=(8, 6))

            # Create a list of colors for the boxplots based on the number of features you have
            boxplots_colors = ['#5AC1A2']

            # Boxplot data
            bp = ax.boxplot(data_frame[column], patch_artist=True, vert=False)

            # Change to the desired color and add transparency
            for patch, color in zip(bp['boxes'], boxplots_colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.4)

            # Create a list of colors for the violin plots based on the number of features you have
            violin_colors = ['#5AC1A2']

            # Violinplot data
            vp = ax.violinplot(data_frame[column], points=500, showmeans=False, showextrema=False, showmedians=False, vert=False)

            for idx, b in enumerate(vp['bodies']):
                # Get the center of the plot
                m = np.mean(b.get_paths()[0].vertices[:, 0])
                # Modify it so we only see the upper half of the violin plot
                b.get_paths()[0].vertices[:, 1] = np.clip(b.get_paths()[0].vertices[:, 1], idx+1, idx+2)
                # Change to the desired color
                b.set_color(violin_colors[idx])

                # Create a list of colors for the scatter plots based on the number of features you have
                scatter_colors = ['#5AC1A2']

                # Scatterplot data
                plt.scatter(data_frame[column], np.ones(len(data_frame[column])), s=3, c=scatter_colors[0])

                plt.yticks([1], [''])  # Set text labels.
                plt.xlabel('Values')
                plt.title(f"Sebaran {column}")

                # Menyimpan plot dalam variabel
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)

                # Menutup plot untuk plot selanjutnya
                plt.close()

                return buffer


        # Menyimpan Plot
        c_temp = plot_kon(day_df, 'temp')
        c_atemp = plot_kon(day_df, 'atemp')
        c_hum = plot_kon(day_df, 'hum')
        c_windspeed = plot_kon(day_df, 'windspeed')
        c_casual = plot_kon(day_df, 'casual')
        c_registered = plot_kon(day_df, 'registered')
        c_cnt = plot_kon(day_df, 'cnt')

        # Menampilkan plot
        c4, c5, c6 = st.columns((1,1,1))
        c7, c8, c9 = st.columns((1,1,1))
        c10 = st.columns((1))

        c4.markdown("**Sebaran Temperatur**")
        c4.image(Image.open(io.BytesIO(c_temp.getvalue())), caption='Caption')

        c5.markdown("**Sebaran Suhu Perasaan**")
        c5.image(Image.open(io.BytesIO(c_atemp.getvalue())), caption='Caption')

        c6.markdown("**Sebaran Kelembapan**")
        c6.image(Image.open(io.BytesIO(c_hum.getvalue())), caption='Caption')
        
        c7.markdown("**Sebaran Kecepatan Angin**")
        c7.image(Image.open(io.BytesIO(c_windspeed.getvalue())), caption='Caption')

        c8.markdown("**Sebaran Pengguna Biasa**")
        c8.image(Image.open(io.BytesIO(c_casual.getvalue())), caption='Caption')

        c9.markdown("**Sebaran Pengguna Terdaftar**")
        c9.image(Image.open(io.BytesIO(c_registered.getvalue())), caption='Caption')
           
        c10.markdown("**Sebaran Total Sepeda yang disewakan**")
        c10.image(Image.open(io.BytesIO(c_cnt.getvalue())), caption='Caption')
            
        # Time Series
        # Convert 'dteday' to datetime
        day_df['dteday'] = pd.to_datetime(day_df['dteday'])

        # Set 'dteday' as index
        day_df.set_index('dteday', inplace=True)

        # Plot the time series
        plt.figure(figsize=(25, 8))
        plt.plot(day_df.index, day_df['cnt'], marker='o', linestyle='-', color='#1380A1')
        plt.title('Data Deret Waktu Dari Sistem berbagi Sepeda ')
        plt.xlabel('Date')
        plt.ylabel('Banyaknya sepeda')
        plt.grid(True)
        plt.show()
        plt1 = plt.gcf()
        st.pyplot(plt1)

        # Interpretasi
        st.caption(
            """
            # Interpretasi
            Jadi gini..
            """
        )

        # Matriks Korelasi 
        df = day_df.iloc[:, 2:]

        # Menghitung matriks korelasi
        corr = df.corr()

        # Plot heatmap
        plt.figure(figsize=(12, 12))
        sns.heatmap(corr, annot=True, cmap='viridis')
        plt.title('Matriks Korelasi')
        plt.show()
        plt2 = plt.gcf()
        st.pyplot(plt2)

        # Interpretasi
        st.caption(
            """
            # Interpretasi
            Jadi gini..
            """
        )

except Exception as e:
    st.error(f"ERROR: Masukkan tanggal dengan benar{e}")
