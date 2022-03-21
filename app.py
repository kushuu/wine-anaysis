'''
let's do this!
'''

import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go


df = st.cache(pd.read_csv)('clean_winesV2.csv')
country_wise_count = df['country_code'].value_counts()

data = dict(
        type = 'choropleth',
        locations = country_wise_count.index,
        z = country_wise_count.values,
        text = list(country_wise_count.index),
        colorbar = {'title' : 'Number of records found'},
      )
layout = dict(
    title = 'Country-wise wine records',
    geo = dict(
            showframe = True,
            projection = {'type':'natural earth'}
    )
)


wineries = st.sidebar.multiselect('Show wineries.', df['winery'].unique())
prices = st.sidebar.multiselect('Show prices.', df['price'].unique())
rating = st.sidebar.multiselect('Show rating.', df['rating'].unique())
category = st.sidebar.multiselect('Show category.', df['category'].unique())

new_df = df[df['winery'].isin(wineries)]
new_df.reset_index(drop = True, inplace = True)
st.write(new_df)

try:
    fig1 = px.scatter(new_df,y='price' ,color='category')
    
    fig2 = px.line(new_df,y='price' ,color='designation')
    
    top_wineries = new_df.winery.value_counts()
    fig3 = px.bar(top_wineries[::-1], orientation='h')
    
    tt = new_df.winery.value_counts().dropna()
    # tt = tt.where(tt.values > 100)
    fig4 = px.pie(tt, values=tt.values, names=tt.index, title='Presence of wineries in the dataset')

    fig5 = px.bar(df.category.value_counts()[::-1], orientation='h')

    fig6 = go.Figure(data = [data],layout = layout)

    fig1.update_xaxes(showgrid = False)
    fig1.update_yaxes(showgrid = False)
    fig2.update_xaxes(showgrid = False)
    fig2.update_yaxes(showgrid = False)
    fig3.update_xaxes(showgrid = False)
    fig3.update_yaxes(showgrid = False)
    fig5.update_xaxes(showgrid = False)
    fig5.update_yaxes(showgrid = False)

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
    st.plotly_chart(fig5)
    st.plotly_chart(fig6)

except KeyError as e:
    print(e)
    print("Nothing to show on the graph right now!\n")