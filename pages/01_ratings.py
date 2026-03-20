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

st.write('Players sorted by rating. You can filter by age or league')

# import databáze

db = pd.read_excel('db.xlsx')

# filtrování dle věku

min_age = int(db['age'].min())
max_age = int(db['age'].max())

age_filter = st.slider('Set player min and max age :', min_value=min_age, max_value=max_age, value=(min_age, max_age))

# filtorvání dle ligy

leagues = sorted(db['league_name'].dropna().unique())
leagues_filter = st.selectbox('Choose preffered league:', options=['All leagues'] + leagues)

# aplikace filtrů

df_filtered = db[(db['age'] >= age_filter[0]) & (db['age'] <= age_filter[1])]

if leagues_filter != 'All leagues':
    df_filtered = df_filtered[df_filtered['league_name'] == leagues_filter]

# výstup 

show_columns = ['player_name', 'birthday', 'position', 'nationality', 'Current Club', 'avg_rating_']
df_final = df_filtered[show_columns].sort_values('avg_rating_', ascending=False)

st.dataframe(df_final, use_container_width=True)