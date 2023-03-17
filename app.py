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
from markdownlit import mdlit

st.set_page_config(layout='wide')

page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(page_bg_img, unsafe_allow_html=True)

mdlit('## Sleep Analysis [blue]Dashboard[/blue]')

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
        c1, c2 = st.columns(2)
        with c1:
            question_url = 'https://assets2.lottiefiles.com/packages/lf20_muyl0kpg.json'
            question_lottie = load_lottieurl(question_url)
            st_lottie(question_lottie,width=200)
        with c2:
            mdlit("### Is this [green]Data[/green] looks appealing ?")
        with st.container():
            left,mid,right = st.columns(3)
            with mid:
                st.markdown('<h3 style="text-align: center;color : orange;">Lets try to visualize it </h3>',unsafe_allow_html=True)
                dropdown_url = "https://assets2.lottiefiles.com/packages/lf20_wsyyln4p.json"
                dropdown_lottie = load_lottieurl(dropdown_url)
                st_lottie(dropdown_lottie,width=200)


def plots(data):
    with st.container():
        sel = st.selectbox('Filter your sleep efficiencies',['Sleep Duration','Caffeine Consumption','Alcohol Consumption','Smoking Status','Exercise Frequency'])
        col1,col2 = st.columns([7,5])
        with col1:
            fig1 = px.histogram(data,x='sleepefficiency',color=''.join(sel.lower().split()),labels = {'sleepefficiency':'Sleep Efficiency'},title='How much duration is enough for efficient sleep ? ⏰⏰')
            st.plotly_chart(fig1)
        with col2:
            fig2 = px.pie(data,names=''.join(sel.lower().split()),title=f'Composition Chart of {sel}',hole=.3)
            st.plotly_chart(fig2)


    with st.container():
        deep_vs_rem = px.scatter(data.dropna(),x='deepsleeppercentage',y='remsleeppercentage',color='alcoholconsumption',size='awakenings',title='😪 Analzing Deep sleep and REM sleep %')
        st.plotly_chart(deep_vs_rem,use_container_width=True)
        col1,col2 = st.columns(2)
        with col1 :
            status = st.selectbox(label=' (%) of men & womens',options = ['Alcohol Consumption','Caffeine Consumption','Exercise Frequency'])
            pie = px.pie(data,names='gender',values=''.join(status.lower().split()),title=f'Males and Females composition of {status}')
            st.plotly_chart(pie)
        with col2:
            fig = px.density_heatmap(data,x='exercisefrequency',y='deepsleeppercentage',text_auto=True,title='💪 Exercise Matters to all 💪')
            st.plotly_chart(fig)





if __name__ == '__main__':
    data = load()
    show_data(data)
    plots(data)
