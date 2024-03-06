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
import base64

# Setting
st.set_page_config(
    page_title="Bikeshare",
    page_icon="🚲",
)

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

Hari = data[(data["dteday"] >= str(start)) & (data["dteday"] <= str(end))]
Date = data[(data["dteday"] >= str(start)) & (data["dteday"] <= str(end))]
cor = data[['cnt','temp','atemp', 'hum', 'windspeed', 'casual', 'registered']]

# Page3
# EKSPLORASI
st.markdown("<h1 style='text-align: center; color: white;'>📊 Eksplorasi Data</h1>", unsafe_allow_html=True)
st.markdown("---")
st.subheader('Jumlah Total')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("  Total Rents", value=count(Date))
with col2:
    st.metric("  Total Membered", value=Date['registered'].sum())
with col3:
    st.metric("  Total Regular", value=Date['casual'].sum())
st.markdown("---")

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
# Membuat tiga kolom
c1, c2, c3 = st.columns((1,1,1))

# Mendefinisikan fungsi untuk menampilkan gambar dengan judul dan caption opsional
def img_capt(column, title, image_bytes, button_label, default_caption):
    # Mengubah objek BytesIO menjadi base64
    encoded_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
    
    column.markdown(f"**{title}**")
    column.image(f"data:image/png;base64,{encoded_image}")
    if column.button(button_label):
        column.write(default_caption)

# Menampilkan gambar dengan judul dan caption opsional di setiap kolom
img_capt(c1, "Sebaran Musim", c_season, "Caption1", 'Dalam periode 2 tahun yang diamati, Musim Gugur mencatat jumlah hari terbanyak dibandingkan dengan musim lainnya, dengan total mencapai 188 hari.')
img_capt(c2, "Sebaran Hari Libur", c_holiday, "Caption2", 'Hari Libur dalam rentang waktu dua tahun terbilang jarang.\nPada hari libur, terdapat hanya 21 hari, sedangkan pada hari biasa, terdapat 710 hari.')
img_capt(c3, "Sebaran Cuaca", c_weathersit, "Caption3", 'Selama dua tahun, cuaca sering berkabut.\nTerjadi 247 hari dengan kondisi cuaca berkabut, 463 hari dengan cuaca cerah, dan hanya 21 hari dengan cuaca salju ringan.')

st.markdown("---")

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
# Membuat tiga kolom
c4, c5, c6 = st.columns((1,1,1))
c7, c8, c9 = st.columns((1,1,1))

img_capt(c4, "Sebaran Temperatur", c_temp, "Caption4", 'Pola distribusi yang bimodal dan simetris menunjukkan variasi suhu yang cukup signifikan. Dengan rata-rata sekitar 20.31, kita bisa melihat bahwa terdapat dua puncak distribusi suhu yang mungkin mencerminkan dua kondisi cuaca yang berbeda.')
img_capt(c5, "Sebaran Suhu Perasaan", c_atemp, "Caption5", 'Distribusi bimodal dengan asimetri menunjukkan adanya variasi signifikan dalam persepsi suhu. Rata-rata suhu perasaan yang lebih rendah mungkin menunjukkan adanya kondisi cuaca yang berpotensi lebih dingin.')
img_capt(c6, "Sebaran Kelembapan", c_hum, "Caption6", 'Distribusi simetris menunjukkan kecenderungan kelembapan yang stabil. Hal ini dapat mempengaruhi persepsi cuaca oleh pengguna, terutama dalam hal kenyamanan.')
img_capt(c7, "Sebaran Kecepatan Angin", c_windspeed, "Caption7", 'Distribusi yang menjulur ke kanan menunjukkan adanya kemungkinan kecepatan angin yang lebih tinggi pada beberapa titik waktu. Hal ini dapat mempengaruhi keamanan dan kenyamanan saat bersepeda.')
img_capt(c8, "Sebaran Pengguna Biasa", c_casual, "Caption8", 'Distribusi data cenderung memiliki ekor panjang ke arah kanan.\nTerdapat 731 data yang diamati, dengan rata-rata sekitar 848.176471 dan standar deviasi sekitar 686.622488. Nilai minimum data adalah 2, sementara nilai maksimumnya mencapai 3410. Distribusi data ini cenderung memiliki ekor panjang ke arah kanan, dengan nilai median (50%) sekitar 713. Quartil pertama (25%) berada di sekitar 315.5, sementara quartil ketiga (75%) berada di sekitar 1096.')
img_capt(c9, "Sebaran Pengguna Terdaftar", c_registered, "Caption9", 'Distribusi yang simetris dan mendekati distribusi normal menunjukkan bahwa pengguna terdaftar memiliki kecenderungan yang lebih merata dalam menggunakan layanan ini. Hal ini bisa mencerminkan kestabilan dalam pola penggunaan sepeda terdaftar.')
    
st.markdown("**Sebaran Total Sepeda yang disewakan**")
st.image(Image.open(io.BytesIO(c_cnt.getvalue())), 
         caption='Distribusi data menunjukkan pola penyebaran yang simetris dan hampir mendekati distribusi normal. Dengan rata-rata sekitar 4504.35 dan standar deviasi sekitar 1937.21, kita bisa melihat bahwa pola penyebaran data ini menunjukkan kecenderungan simetris dan hampir menyerupai distribusi normal. Hal ini mungkin mencerminkan kestabilan dalam pola penggunaan sepeda yang disewakan, dengan jumlah yang relatif merata di berbagai waktu.')

st.markdown("---")

# Time Series
st.write("\n\n")
st.subheader('Data Deret Waktu')

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
if st.button("Interpretasi 1"):   
    st.write("Data deret waktu dari rentang 2011 hingga 2012 menunjukkan fluktuasi yang signifikan dalam jumlah total sepeda yang disewakan. Meskipun terjadi fluktuasi, terdapat kecenderungan peningkatan jumlah total sepeda yang disewakan seiring berjalannya waktu. Hal ini menunjukkan adanya pertumbuhan atau peningkatan permintaan terhadap layanan sewa sepeda selama periode tersebut.")

# Matriks Korelasi 
st.write("\n\n")
st.subheader('Matriks Korelasi')
df = day_df.iloc[:, -7:]

# Plot heatmap
def corrfunc(x, y, **kws):
  r, p = stats.pearsonr(x, y)
  p_stars = ''
  if p <= 0.05:
    p_stars = '*'
  if p <= 0.01:
    p_stars = '**'
  if p <= 0.001:
    p_stars = '***'
  ax = plt.gca()
  ax.annotate('r = {:.2f} '.format(r) + p_stars,
              xy=(0.05, 0.9), xycoords=ax.transAxes)

def annotate_colname(x, **kws):
  ax = plt.gca()
  ax.annotate(x.name, xy=(0.05, 0.9), xycoords=ax.transAxes,
              fontweight='bold')

def cor_matrix(df):
  g = sns.PairGrid(df, palette=['red'], diag_sharey=False)
  # Use normal regplot as `lowess=True` doesn't provide CIs.
  # Upper
  g.map_upper(sns.regplot, scatter_kws={'s': 20, 'color': 'DarkCyan'}, line_kws={'color': '#472a7a'}) 
  # Diag
  g.map_diag(sns.histplot, kde=True, kde_kws=dict(cut=3), alpha=.7, color='teal', edgecolor='black')
  g.map_diag(annotate_colname)
  # Lower
  g.map_lower(sns.kdeplot, cmap='viridis')
  g.map_lower(corrfunc)
  # Remove axis labels, as they're in the diagonals.
  for ax in g.axes.flatten():
    ax.set_ylabel('')
    ax.set_xlabel('')
  return g

st.pyplot(cor_matrix(df))

# Interpretasi
if st.button("Interpretasi 2"):   
    st.write("Insight dari matriks korelasi menunjukkan bahwa peubah registered memiliki korelasi positif yang paling kuat dengan variabel respons cnt, sedangkan peubah hum memiliki korelasi negatif yang paling lemah. Ini menunjukkan bahwa jumlah sepeda yang disewakan yang didaftarkan (registered) memiliki keterkaitan yang erat dengan total jumlah sepeda yang disewakan secara keseluruhan (cnt), sedangkan kelembapan udara (hum) memiliki korelasi yang paling lemah dengan jumlah total sepeda yang disewakan.")
