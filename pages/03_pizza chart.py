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

st.write('Select specific player to show his pizza chart')

# import databáze

db = pd.read_excel('db.xlsx')

# filtrování ligy

league = st.selectbox('Select league:', sorted(db['league_name'].unique()))
filtered_league = db[db['league_name'] == league]

# filtr pro hráče, kteří odehráli alespoň 600 minut

filtered_league = filtered_league[filtered_league['minutes_played'] >= 600]

# výběr sloupců 

radar_cols = ['goals_per_90', 'xg_per_90', 'shots_on_target_per_90', 'dribbles_successful_per_90', 'dribbled_past_per_90',
              'assists_per_90', 'xa_per_90', 'passes_completed_per_90', 'key_passes_per_90', 'accurate_crosses_per_90',
              'duels_per_90', 'duels_won_per_90', 'aerial_duels_won_per_90', 'interceptions_per_90', 'blocks_per_90'
]

# ošetření NaN hodnot
filtered_league[radar_cols] = filtered_league[radar_cols].fillna(0)

# výpočet percentilů podle pozice hráč

for pos in filtered_league['position'].unique():
    df_pos = filtered_league[filtered_league['position'] == pos]
    for col in radar_cols:
        filtered_league.loc[df_pos.index, col + '_pct'] = df_pos[col].rank(pct=True)

# filtrování klubu

team = st.selectbox('Select club:', sorted(filtered_league['Current Club'].unique()))
filtered_club = filtered_league[filtered_league['Current Club'] == team]

# výběr konkrétního hráče

player = st.selectbox('Select player:', sorted(filtered_club['player_name'].unique()))
filtered_player = filtered_club[filtered_club['player_name'] == player]

# příprava dat pro pizza chart

labels = radar_cols
values = [filtered_player[col + '_pct'] for col in radar_cols]
