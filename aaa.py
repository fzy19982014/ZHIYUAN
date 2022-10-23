import pandas as pd
import streamlit as st
import numpy as np
import datetime
import math

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot

# Import data
path=r'C:\Users\Zhiyuan\Downloads\owid-covid-data.csv'
path_dic=r'C:\Users\Zhiyuan\Downloads\owid-covid-codebook.csv'
covid=pd.read_csv(path)
dic=pd.read_csv(path_dic)

# Change the form of the date
covid['date']=pd.to_datetime(covid['date'])   

# Calculate the death rate 
covid['death_rate']=covid['total_deaths']/covid['total_cases']

# Calculate the vaccinated rate
covid['vaccinations_rate']=covid['people_vaccinated']/covid['population'] 

# Location
countries=list(covid['location'].unique())

# Map Function
def mapfunction():
        covid1=covid.copy()
        covid1['date']=covid1['date'].dt.strftime('%Y-%m-%d')
        
        fig = px.choropleth(covid1,
        locations="location",
        locationmode = "country names",
        color="death_rate",
        hover_name="location",
        animation_frame="date")
    
        fig.update_layout(
        title_text = 'Death rate in different countries overtime',
        title_x = 0.5,
        geo=dict(
        showframe = False,
        showcoastlines = False, ))
    
        return fig

covid['infection_rate']=covid['total_cases']/covid['population']
def mapfunction1():
        covid1=covid.copy()
        covid1['date']=covid1['date'].dt.strftime('%Y-%m-%d')
        
        fig1 = px.choropleth(covid1,
        locations="location",
        locationmode = "country names",
        color="infection_rate",
        hover_name="location",
        animation_frame="date")
    
        fig1.update_layout(
        title_text = 'Infection rate in different countries overtime',
        title_x = 0.5,
        geo=dict(
        showframe = False,
        showcoastlines = False, ))
    
        return fig1

def mapfunction2():
        covid1=covid.copy()
        covid1['date']=covid1['date'].dt.strftime('%Y-%m-%d')
        
        fig2 = px.choropleth(covid1,
        locations="location",
        locationmode = "country names",
        color="vaccinations_rate",
        hover_name="location",
        animation_frame="date")
    
        fig2.update_layout(
        title_text = 'Vaccinations rate in different countries overtime',
        title_x = 0.5,
        geo=dict(
        showframe = False,
        showcoastlines = False, ))
    
        return fig2
       
# Death rate visulize
def death_rate_visulize(location):
        fig3=px.line(covid[covid['location']==location],x='date',y='death_rate',color='location')
        
        fig3.update_layout(
        title_text = 'Death rate',
        title_x = 0.5,
        geo=dict(
        showframe = False,
        showcoastlines = False, ))   
        
        return fig3
    
# vaccinated rate visulize
def vac_visulize(location):
        fig4=px.line(covid[covid['location']==location],x='date',y='vaccinations_rate',color='location')
        
        fig4.update_layout(
        title_text = 'Vaccinations rate',
        title_x = 0.5,
        geo=dict(
        showframe = False,
        showcoastlines = False, )) 
        
        return fig4

# Infection rate visulize
def infection_rate(location):
        fig5=px.line(covid[covid['location']==location],x='date',y='infection_rate',color='location')
        
        fig5.update_layout(
        title_text = 'Infection rate',
        title_x = 0.5,
        geo=dict(
        showframe = False,
        showcoastlines = False, )) 
       
        return fig5
    
   

#### Title
st.title('COVID-19 Dashboard') 
st.text('made by QBUS6860 Group 53')


# Sidebar
st.sidebar.write('NAVIGATION')
NAVIGATION=st.sidebar.selectbox('Please select one dashboard',('Overview','Single Country'))

## Overview
if NAVIGATION == 'Overview':
    overview = st.container()
    with overview:
        st.header ('Overview')
        st.text('As of June 29, 2022')
        
        # Figure setting
        col1, col2, col3 =st.columns(3)
        
        # Total new cases
        total_new_case=covid[covid['date']== pd.to_datetime('2022-06-29')]['new_cases'].sum()
        total_new_case_yesterday=covid[covid['date']== pd.to_datetime('2022-06-28')]['new_cases'].sum()
        total_new_case_change=str(round(100* (total_new_case / total_new_case_yesterday) -1 , 2))
        
        # Total new death 
        total_new_death=covid[covid['date']== pd.to_datetime('2022-06-29')]['new_deaths'].sum()
        total_new_death_yesterday=covid[covid['date']== pd.to_datetime('2022-06-28')]['new_deaths'].sum()
        total_new_death_change=str(round(100* (total_new_death / total_new_death_yesterday) -1 , 2))
        
        #Total new vaccination
        total_new_vaccination=covid[covid['date']== pd.to_datetime('2022-06-29')]['new_vaccinations'].sum()
        total_new_vaccination_yesterday=covid[covid['date']== pd.to_datetime('2022-06-28')]['new_vaccinations'].sum()
        total_new_vaccination_change=str(round(100* (total_new_vaccination / total_new_vaccination_yesterday) -1 , 2))
        
        # column metric
        col1.metric(label = 'Total New Cases', value= str(int(total_new_case/1000))+ 'k', delta = total_new_case_change + '%')
        col2.metric(label = 'Total New Deaths', value= str(int(total_new_death/1000))+ 'k', delta = total_new_death_change + '%')
        col3.metric(label = 'Total New vaccinations', value= str(int(total_new_vaccination/1000))+ 'k', delta = total_new_vaccination_change + '%')
      
        # Map visualize
        ##
        
        st.subheader('Infection rate')
        st.plotly_chart(mapfunction1(),use_container_width=True)
        
        st.subheader('Death rate')
        st.plotly_chart(mapfunction(),use_container_width=True)
        
        st.subheader('Vaccinations rate')
        st.plotly_chart(mapfunction2(),use_container_width=True)
    
   
        
        
## Single Country page
if NAVIGATION == 'Single Country':
    cc = st.container()
    with cc:
        st.header ('Single Country')
        st.text('As of June 29, 2022')
        location= st.selectbox('Select on Country',countries)
        
        #Figure setting
        col1, col2, col3= st.columns(3)
        
        # Total cases
        total_case = covid[covid['location'] == location]['total_cases'].values[-1]
        try:
            total_case = str(int(total_case/1000)) + 'k'
        except:
            total_case = 'Not Available'
         
        # Total vaccination
        total_vaccination = covid[covid['location'] == location]['people_vaccinated'].values[-1]
        try:
            total_vaccination = str(int(total_vaccination/1000)) + 'k'
        except:
            total_vaccination = 'Not Available' 
                              
        # Total death
        total_death = covid[covid['location'] == location]['total_deaths'].values[-1]
        try:
            total_death = str(int(total_death/1000)) + 'k'
        except:
            total_death = 'Not Available'  
            
        # column metrix 
        col1.metric(label = 'Total Cases', value = total_case)
        col2.metric(label = 'Total Vaccinations', value = total_vaccination)
        col3.metric(label = 'Total Deaths', value = total_death)
        
        # chart
        st.subheader('Infection rate in '+location)
        st.plotly_chart(infection_rate(location), use_container_witdth = True)

        st.subheader('Death rate in '+location)
        st.plotly_chart(death_rate_visulize(location), use_container_witdth = True)
        
        st.subheader('Vaccinations rate in '+location)
        st.plotly_chart(vac_visulize(location), use_container_witdth = True)





