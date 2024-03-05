# streamlit run hello-world.py
import streamlit as st 
import pandas as pd

# TEXT
# markdown()
st.write(
    """
    # My first app
    Hello, para calon praktisi data masa depan!
    """
)

# title()
st.title('Belajar Analisis Data')
# header()
st.header('Pengembangan Dashboard')
# subheader()
st.subheader('Pengembangan Dashboard')
# caption()
st.caption('Copyright (c) 2023')
# code()
code = """def hello():
    print("Hello, Streamlit!")"""
st.code(code, language='python')
# text()
st.text('Halo, calon praktisi data masa depan.')
# latex()
st.latex(r"""
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
""")

# DATA DISPLAY
# Write
st.write(pd.DataFrame({
    'c1': [1, 2, 3, 4],
    'c2': [10, 20, 30, 40],
}))

# dataframe()
sample_data = {
    'name': ['John', 'Alia', 'Ananya', 'Steve', 'Ben'],
    'age': [24, 22, 23, 25, 28],  
    'communication_skill_score': [85, 70, 75, 90, 90],
    'quantitative_skill_score': [80, 90, 80, 75, 70]
}
 
df = pd.DataFrame(sample_data)

st.dataframe(data=df, width=500, height=150)

# table()
st.table(data=df)

# metric()
st.metric(label="Temperature", value="28 °C", delta="1.2 °C")

# json()
st.json({
    'c1': [1, 2, 3, 4],
    'c2': [10, 20, 30, 40],
})


# CHART
import matplotlib.pyplot as plt
import numpy as np
 
x = np.random.normal(15, 5, 250)
 
fig, ax = plt.subplots()
ax.hist(x=x, bins=15)
st.pyplot(fig)

# -----
# WIDGET
# TEXT INPUT
name = st.text_input(label='Nama lengkap', value='')
st.write('Nama: ', name)

# Text Area
text = st.text_area('Feedback')
st.write('Feedback: ', text)

# Number input
number = st.number_input(label='Umur')
st.write('Umur: ', int(number), ' tahun')

# Date input
date = st.date_input(label='Tanggal lahir', min_value=datetime.date(1900, 1, 1))
st.write('Tanggal lahir:', date)

# File Uploader
uploaded_file = st.file_uploader('Choose a CSV file')
 
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

# Camera Input
picture = st.camera_input('Take a picture')
if picture:
    st.image(picture)

# BUTTON WIDGETS
# Button
    
