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
        text = list(df.country.value_counts().index),
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
category = st.sidebar.multiselect('Show category.', df['category'].unique())

new_df = df[df['winery'].isin(wineries)]
new_df.reset_index(drop = True, inplace = True)
st.write(new_df)
top_wineries = new_df.winery.value_counts()
tt = new_df.winery.value_counts().dropna()
winery_price = new_df[(new_df.price >= 14) & (new_df.price <= 42)][['winery', 'price']].dropna()
wine_price = new_df[(new_df.price >= 14) & (new_df.price <= 42)][['wine', 'price']].dropna()
wnry_agg = winery_price.groupby('winery').agg({'price' : 'mean'})

try:
    fig1 = px.line(new_df,y='price' ,color='category', markers=True, title="Price for different categories", labels={
            'price' : 'price ($)',
            'category' : 'wine category'
        }
    )

    fig2 = px.line(new_df,y='price' ,color='designation', markers=True, title="Price for different designations", labels={
            'price' : 'price ($)'
        }
    )
    fig3 = px.line(wnry_agg, markers=True, title="Average price of selected wineries", labels={
            'value' : 'price ($)'
        }
    )
    fig4 = px.bar(top_wineries[::-1], orientation='h', title="Distribution of reviews of wineries", labels= {
            'index' : 'winery',
            'value' : 'count'
        }
    )
    fig5 = px.pie(tt, values=tt.values, names=tt.index, title='Presence of wineries in the dataset')
    fig6 = px.bar(new_df.category.value_counts()[::-1], orientation='h', title="Categories offered by the selected wineries.", labels= {
            'index' : 'category',
            'value' : 'count'
        }
    )
    fig7 = go.Figure(data = [data],layout = layout)
    fig7.update_layout(
        title = "Geoplot of the reviews in our dataset"
    )
    if category:
        df_spe = df[df.category.isin(category)]
        fig_spe = px.bar(df_spe.category.value_counts(), orientation='h', title="Distribution of selected categories", labels= {
                'index' : 'category',
                'value' : 'count'
            }
        )

    fig1.update_xaxes(showgrid = False)
    fig1.update_yaxes(showgrid = False)
    fig2.update_xaxes(showgrid = False)
    fig2.update_yaxes(showgrid = False)
    fig3.update_xaxes(showgrid = False)
    fig3.update_yaxes(showgrid = False)
    fig4.update_xaxes(showgrid = False)
    fig4.update_yaxes(showgrid = False)
    fig5.update_xaxes(showgrid = False)
    fig5.update_yaxes(showgrid = False)
    fig6.update_xaxes(showgrid = False)
    fig6.update_yaxes(showgrid = False)
    if category:
        fig_spe.update_xaxes(showgrid = False)
        fig_spe.update_yaxes(showgrid = False)


    if wineries:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig6, use_container_width=True)
        if category:
            # print(df_spe.category.value_counts())
            st.plotly_chart(fig_spe, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)
        st.plotly_chart(fig5, use_container_width=True)
        st.plotly_chart(fig7, use_container_width=True)

except KeyError as e:
    print(e)
    print("Nothing to show on the graph right now!\n")