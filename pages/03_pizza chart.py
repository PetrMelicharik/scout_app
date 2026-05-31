import streamlit as st
import pandas as pd
from urllib.request import urlopen
import matplotlib.pyplot as plt
from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
from pathlib import Path

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

def load_db():
    return pd.read_excel('db.xlsx')

db = load_db()

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

pretty_labels = {
    'goals_per_90': 'Goals',
    'xg_per_90': 'xG',
    'shots_on_target_per_90': 'Shots on Target',
    'dribbles_successful_per_90': 'Successful Dribbles',
    'dribbled_past_per_90': 'Dribbled Past',
    'assists_per_90': 'Assists',
    'xa_per_90': 'xA',
    'passes_completed_per_90': 'Completed Passes',
    'key_passes_per_90': 'Key Passes',
    'accurate_crosses_per_90': 'Accurate Crosses',
    'duels_per_90': 'Duels',
    'duels_won_per_90': 'Duels Won',
    'aerial_duels_won_per_90': 'Aerial Duels Won',
    'interceptions_per_90': 'Interceptions',
    'blocks_per_90': 'Blocks'
}


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

# tlačítko
generate = st.button("Generate chart")

if generate:
    # příprava dat pro pizza chart

    labels = [pretty_labels[col] for col in radar_cols]
    values = [filtered_player[col + '_pct'].iloc[0] for col in radar_cols]

    # import fontů

    font_normal = FontManager(Path("fonts/Roboto-Regular.ttf").resolve().as_uri())
    font_bold = FontManager(Path("fonts/RobotoSlab.ttf").resolve().as_uri())
    font_italic = FontManager(Path("fonts/Roboto-Italic.ttf").resolve().as_uri())

    # příprava obrázku

    logo = Image.open('logo.png')

    # paramatry a hodnoty

    params = labels
    values = [int(round(float(v) * 100, 0)) for v in values]

    # barvy výsečí 

    slice_colors = ["#1A78CF"] * 5 + ["#FF9300"] * 5 + ["#D70232"] * 5
    text_colors = ["#000000"] * 10 + ["#F2F2F2"] * 5

    # styl grafu

    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#EBEBE9",     # background color
        straight_line_color="#EBEBE9",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )

    # vykreslení grafu

    fig, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(8, 8.5),                # adjust figsize according to your need
        color_blank_space="same",        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#F2F2F2", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
         color="#000000", fontsize=10,
            fontproperties=font_normal.prop, va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=10,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values
    )

    fig.patch.set_facecolor("white")

    # hlavička grafu

    tittle_text = f"{filtered_player['player_name'].iloc[0]} - {filtered_player['position'].iloc[0]} - {filtered_player['Current Club'].iloc[0]}"

    fig.text(
        0.515, 0.975, tittle_text, size=16,
        ha='center', fontproperties=font_bold.prop, color='#000000'
    )

    # informace pod hlavičku

    tittle2 = f"Season {filtered_player['season'].iloc[0]} {filtered_player['league_name'].iloc[0]} - Percentile Rank - Values per 90 - Min 600 mins played"

    fig.text(
        0.515, 0.953,tittle2, size=13,
        ha="center", fontproperties=font_bold.prop, color="#000000"
    )

    # text vysvětlivky
    fig.text(
        0.34, 0.925, "Attacking        Possession       Defending", size=14,
        fontproperties=font_bold.prop, color="#000000"
    )

    # barvy k vysvětlivkám
    fig.patches.extend([
        plt.Rectangle(
            (0.31, 0.9225), 0.025, 0.021, fill=True, color="#1a78cf",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.462, 0.9225), 0.025, 0.021, fill=True, color="#ff9300",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.632, 0.9225), 0.025, 0.021, fill=True, color="#d70232",
            transform=fig.transFigure, figure=fig
        ),
    ])

    # přidání loga

    ax_image = add_image(
        logo, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
    )

    st.pyplot(fig)

    # stažení grafu

    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)

    # tlačítko pro stažení
    st.download_button(
        label="📥 Download chart",
        data=buf,
        file_name=f"{filtered_player['player_name'].iloc[0]}_radar.png",
        mime="image/png"
    )
