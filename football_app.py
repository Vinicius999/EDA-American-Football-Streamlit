import streamlit as st
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns

st.title('NFL Football Stats (Rushing) ')

st.markdown('''
This app performs simple webscrapping of NFL Football player stats data (focusing on Rushing)!
* **Python libraries:** streamlit, base64, pandas, numpy, matplotlib, seaborn
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
''')

st.sidebar.header('User Input Feature')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2022))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm
@st.cache
def load_data(year):
    url = f'https://www.pro-football-reference.com/years/{year}/rushing.htm'
    html = pd.read_html(url, header = 1)
    df = html[0]
    raw = df.drop(df[df['Age'] == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    
    return playerstats

playerstats = load_data(selected_year)

sorted_unique_team = sorted(playerstats['Tm'].unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Team selection
unique_pos = ['RB', 'QB', 'WR', 'FB', 'TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data

