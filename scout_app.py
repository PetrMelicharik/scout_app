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

# úvod
st.markdown('### Welcome to the FM Scouts app!')
st.write('With this app you can scout and analyze players from these leagues:')

flags = [
    ("at.png", "Austrian Bundesliga"),
    ("at.png", "Austrian 2nd league"),
    ("ba.png", "Bosnian Premier League"),
    ("bg.png", "Bulgarian First League"),
    ("hr.png", "Croatian 1st HNL"),
    ("hr.png", "Croatian 2nd HNL"),
    ("cz.png", "Czechia 1st Chance Liga"),
    ("dk.png", "Danish Superliga"),
    ("dk.png", "Danish 1st Division"),
    ("ee.png", "Estonian Meistrliiga"),
    ("fi.png", "Finnish Veikkausliiga"),
    ("hu.png", "Hungarian NB I"),
    ("lv.png", "Latvian Virsliga"),
    ("no.png", "Norwegian Eliteserien"),
    ("pl.png", "Polish Ekstraklasa"),
    ("pl.png", "Polish 1st League"),
    ("ro.png", "Romanian Liga I"),
    ("ro.png", "Romanian Liga II"),
    ("rs.png", "Serbian SuperLiga"),
    ("rs.png", "Serbian First League"),
    ("sk.png", "Slovak Niké Liga"),
    ("si.png", "Slovenian PrvaLiga"),
    ("se.png", "Swedish Allsvenskan"),   
    ("se.png", "Swedish Superettan"),
    ("ua.png", "Ukraine Premier League")
]

for flag, name in flags:
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image(f"flags/{flag}", width=24)
    with col2:
        st.write(name)





