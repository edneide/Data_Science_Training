import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)

# Function to read the dataset
def get_data(path):
    data = pd.read_csv(path)

    return data

@st.cache( allow_output_mutation=True )
def get_geofile( url ):
 geofile = geopandas.read_file( url )
 return geofile

# Get data
path = 'datasets/kc_house_data.csv'
data = get_data(path)

# Get geofile
url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
geofile = get_geofile( url )

# add new feature
data['price_m2'] = data['price']/data['sqft_lot']

# ============================
# Data overview
# ============================
f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
f_zipcode =  st.sidebar.multiselect('Enter zipcode',
                                    data['zipcode'].unique())

st.title('Data Overview')

if(f_zipcode != []) & (f_attributes != []):
    data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

elif(f_zipcode != []) & (f_attributes == []):
    data = data.loc[data['zipcode'].isin(f_zipcode), :]

elif (f_zipcode == []) & (f_attributes != []):
    data = data.loc[:, f_attributes]

else:
    data = data.copy()

# Descriptive statistics
df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

# merge
m1 = pd.merge(df1, df2, on='zipcode', how='inner')
m2 = pd.merge(m1, df3, on='zipcode', how='inner')
df = pd.merge(m2, df4, on='zipcode', how='inner')

df.columns = ['zipcode', 'total houses', 'price', 'sqrt living',
              'price/m2']


num_attributes = data.select_dtypes(include=['int64', 'float64'])
media = pd.DataFrame(num_attributes.apply(np.mean))
mediana = pd.DataFrame(num_attributes.apply(np.median))
std = pd.DataFrame(num_attributes.apply(np.std))

max_ = pd.DataFrame(num_attributes.apply(np.max))
min_ = pd.DataFrame(num_attributes.apply(np.min))

df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()
df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

st.dataframe(data)

col1, col2 = st.columns(2)

col1.header('Average Values')
with col1:
    st.dataframe(df, height=600, width=800)

col2.header('Descriptive Analysis')
with col2:
    st.dataframe(df1, height=600, width=800)

# ============================
# Densidade de Portfolio
# ============================
st.title('Region Overview')

c1, c2 = st.columns((1, 1))
c1.header('Portfolio Density')

df = data.sample(10)

# Base Map- Folium
density_map = folium.Map(location=[df['lat'].mean(),
                                   df['long'].mean()],
                         default_zoom_start=15)

with c1:
    folium_static(density_map)








