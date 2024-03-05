# streamlit run coba.py
import streamlit as st
import time
import pandas as pd
import seaborn as sns
# pip install scikit-learn
# pip intall scikit-learn decomposition
from sklearn.decomposition import PCA
from scipy import stats
import matplotlib.pyplot as plt

st.set_page_config(page_title='Final Project',  layout='wide')

#this is the header
t1,  = st.columns(1) 

t1.title("Courses Materials application on the *Bike Sharing Dataset*")

# Data used
df = pd.read_csv("dashboard/main_data.csv")

m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))
m1.write('')
m2.metric(label ='Data used',value = "hourly data")
m3.metric(label ='Total data',value = str(len(df)))
m4.metric(label = 'Identified as Outlier',value = str(702))
m1.write('')


cw1, cw2 = st.columns((2.5, 1.7))

cw1.markdown("Dataframe")
cw1.dataframe(df)
cw1.markdown(
"The dataframe's consisted of 17 columns, judging by `dteday` column, we can say the data falls into time series category. The reason's due to the data points are collected or recorded in chronological order."
)
cw2.markdown("Data Type")
cw2.dataframe(pd.DataFrame({"data type": df.dtypes, "Total of missing value": list(df.isna().sum())}))

df=df.iloc[:,2:]

g1, g2 = st.columns((1,1))

g1.markdown(
"Correlation: "
)
corr = pd.DataFrame([[round(j, 3) for j in i] for i in df.corr().values], columns=df.columns, index=df.columns)
theplot=sns.heatmap(corr, annot=True, annot_kws={'size': 4})
g1.pyplot(theplot.get_figure())
g1.markdown(
'''
Summary:
1. `temp` and `atemp` have a high positive correlation of 0.988.
2. `registered` and `cnt` are strongly positively correlated with a coefficient of 0.972.
3. `season` and `mnth` exhibit a notable positive correlation of 0.83.
4. `casual` and `cnt` are moderately positively correlated with a coefficient of 0.695.
5. `casual` and `registered` show a moderate positive correlation of 0.507.
6. `temp` and `casual` have a moderate positive correlation of 0.46.
7. `atemp` and `casual` also have a moderate positive correlation, with a coefficient of 0.454.
8. `weathersit` and `hum` demonstrate a moderate positive correlation of 0.418.
9. `temp` and `cnt` have a moderate positive correlation of 0.405.
10. `atemp` and `cnt` exhibit a similar moderate positive correlation of 0.401.
'''
)
g2.markdown("Outlier: ")

no_categorical = df
thepca = PCA(2)
thepca.fit(no_categorical)
df_reduced = thepca.transform(no_categorical)
idk=pd.DataFrame(df_reduced)
# Calculate Z-scores for each column
z_scores_column1 = stats.zscore(idk[0])
z_scores_column2 = stats.zscore(idk[1])

threshold = 3
# Identify rows with at least one outlier in either column
outliers_rows = idk[(abs(z_scores_column1) > threshold) | (abs(z_scores_column2) > threshold)]

#visualization
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.grid("on", alpha=0.3)
ax.scatter(df_reduced[0:,0], df_reduced[0:,1], c="blue", alpha=0.6, label=f'observation: {len(df_reduced)-len(outliers_rows)}')
ax.scatter(outliers_rows[0], outliers_rows[1], c="orange", alpha=0.6, label=f'outlier observation: {len(outliers_rows)}')
ax.legend(loc="upper right")
ax.set_title("reduced to 2 dimension")
g2.pyplot(fig)


# Contact Form
with st.expander("Summary"):
    st.markdown(
        '''
        the data that's used on this notebook is considered as time series due to the data's collected or recorded over a sequence of time intervals. The dataset's consisted of 17 columns ('dteday', 'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt') where they appear as numerical at first, however when we saw it deeply the type of many columns on the dataset are converted categorical type. On the exploration, it's clear that few variables correlate to each others. As there are only 10 column combinations in which their correlation is higher than 0.4. When we tried to reduce its dimension into a dimension where's possible to be visualized. It could be stated, there are also a lot of outliers on the dataset.
        '''
    )
    
# Contact Form
with st.expander("Contact me"):
    with st.form(key='contact', clear_on_submit=True):
        
        email = st.text_input('Contact Email')
        st.text_area("Query","Write here if yo wanna contact me")
        
        submit_button = st.form_submit_button(label='Send Information')  