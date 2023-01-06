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
df_selected_team = playerstats[(playerstats['Tm'].isin(selected_team)) & (playerstats['Pos'].isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write(f'Data Dimension: {df_selected_team.shape[0]} rows and {df_selected_team.shape[1]} columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.buttom('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')
    
    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()
