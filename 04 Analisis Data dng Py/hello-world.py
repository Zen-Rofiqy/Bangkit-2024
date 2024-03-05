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

