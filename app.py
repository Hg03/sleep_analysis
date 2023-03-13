import streamlit as st
from streamlit_lottie import st_lottie
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_plotly_events import plotly_events
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import numpy as np

st.set_page_config(layout='wide')
st.title('Sleep Analysis Dashboard')

@st.cache_data
def load():
    df = pd.read_csv('data/sleep.csv')
    df.rename(columns={'ID':'id','Age':'age','Gender':'gender','Bedtime':'bedtime','Wakeup time':'wakeuptime','Sleep duration':'sleepduration','Sleep efficiency':'sleepefficiency','REM sleep percentage':'remsleeppercentage','Deep sleep percentage':'deepsleeppercentage','Light sleep percentage':'lightsleeppercentage','Awakenings':'awakenings','Caffeine consumption':'caffeineconsumption','Alcohol consumption':'alcoholconsumption','Smoking status':'smokingstatus','Exercise frequency':'exercisefrequency'},inplace=True)
    return df

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_data(data):
    col1,col2 = st.columns(2)
    gd = GridOptionsBuilder.from_dataframe(data)
    gd.configure_pagination(enabled=True,paginationPageSize=10,paginationAutoPageSize=10)
    gd.configure_default_column(editable=True,groupable=True,filterable=True)
    gridOptions = gd.build()
    with col1:
        with st.expander('Sample Data'):
            grid_table = AgGrid(data, gridOptions = gridOptions, enable_enterprise_modules = True,update_mode = GridUpdateMode.SELECTION_CHANGED,height=400)
    with col2:
        question_url = 'https://assets3.lottiefiles.com/packages/lf20_vyrigtxe.json'
        question_lottie = load_lottieurl(question_url)
        st_lottie(question_lottie)
        st.markdown("<h3 style='text-align: center; color: black;'>⬅️ Is this Data looks appealing ??</h3>", unsafe_allow_html=True)

def plots(data):
    with st.container():
        sel = st.selectbox('Filter your sleep efficiencies',['Sleep Duration','Caffeine Consumption','Alcohol Consumption','Smoking Status','Exercise Frequency'])
        col1,col2 = st.columns([7,5])
        with col1:
            fig1 = px.histogram(data,x='sleepefficiency',color=''.join(sel.lower().split()),labels = {'sleepefficiency':'Sleep Efficiency'},title='How much duration is enough for efficient sleep ?')
            st.plotly_chart(fig1)
        with col2:
            fig2 = px.pie(data,names=''.join(sel.lower().split()),title=f'Composition Chart of {sel}',hole=.3)
            st.plotly_chart(fig2)


    with st.container():
        deep_vs_rem = px.scatter(data,x='deepsleeppercentage',y='remsleeppercentage',color='gender',size='sleepduration',title='Analzing Deep sleep and REM sleep %')
        st.plotly_chart(deep_vs_rem,use_container_width=True)
        col1,col2 = st.columns(2)
        with col1 :

            fig = go.Figure(data=[go.Mesh3d(x=data.deepsleeppercentage.tolist(),y=data.remsleeppercentage.tolist(),z=data.sleepefficiency,opacity=0.5,color='green',)])
            fig.update_layout(title='Deep Sleep Vs REM sleep Vs Sleep Efficiency')
            st.plotly_chart(fig)
        
        with col2:
            fig = px.density_heatmap(data,x='exercisefrequency',y='deepsleeppercentage',text_auto=True,title='Exercise Matters to all ')
            st.plotly_chart(fig)





if __name__ == '__main__':
    data = load()
    show_data(data)
    plots(data)
