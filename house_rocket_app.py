import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('House Rocket Company')
st.markdown('Welcome to House Rocket Data Analysis')

st.header('Load data')

# read data
@st.cache(allow_output_mutation=True)

def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])

    return data

# load data
data = get_data('datasets/kc_house_data.csv')

# transformaitons

# waterfront
data['water_front_cat'] = 'NA'
data['water_front_cat'] = data['waterfront'].apply(lambda x: 'Yes' if x == 1 else 'No')


# Filters

st.sidebar.title('Filters')

# filter bedrooms
bedrooms_filter = st.sidebar.multiselect(
    'Number of Bedrooms',
    data['bedrooms'].unique()
)

#st.write('Your filter is', bedrooms_filter)
#st.write(type(bedrooms_filter))

# filter waterfront
waterfront_select = st.sidebar.selectbox(
    label='Is the place waterfront?',
    options=('Yes', 'No'),
    index=1
)


# plot mapa
st.title('House Rocket Map')
is_checked = st.sidebar.checkbox('Display Map')

# filters
price_min = int(data['price'].min())
price_max = int(data['price'].max())
price_avg = int(data['price'].mean())

price_slider = st.sidebar.slider('Price Range',
                         price_min,
                         price_max,
                         price_avg)

if is_checked:
    # select rows
    houses = data[(data['price'] < price_slider) &
                  (data['bedrooms'].isin(bedrooms_filter)) &
                  (data['water_front_cat'] == waterfront_select)][['id', 'lat', 'long', 'price', 'bedrooms']]

    #st.dataframe(houses)

    # draw map
    fig = px.scatter_mapbox(
        houses,
        lat='lat',
        lon='long',
        size='bedrooms',
        color='price',
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=10
    )

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=600, margin={"r":0, "t":0, "l":0, "b":0})
    st.plotly_chart(fig)