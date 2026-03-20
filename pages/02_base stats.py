import streamlit as st
import pandas as pd

# nastavení stránky - kosmetická úprava
st.set_page_config(page_title='FM Scouts app', page_icon='⚽')

# nadpis a logo v jednom řádku
col1, col2 = st.columns([4, 1])

with col1:
    st.title('FM Scouts app')

with col2:
    st.image('logo.jpg', width=80)

st.write('Player stats by specific league')

# import databáze

db = pd.read_excel('db.xlsx')

# ligový filtr

leagues = sorted(db['league_name'].dropna().unique())
leagues_filter = st.selectbox('Choose preffered league:', options=['Choose league'] + leagues)

# aplikace filtru

if leagues_filter != 'All leagues':
    df_filtered = db[db['league_name'] == leagues_filter]

# góly 

st.write('Goals')
df_goals = df_filtered[['player_name', 'Current Club', 'goals']].sort_values('goals', ascending=False).head(10)
st.dataframe(df_goals, use_container_width=True)