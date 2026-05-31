import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
import random

# nastavení stránky - kosmetická úprava
st.set_page_config(page_title='FM Scouts app', page_icon='⚽')

# nadpis a logo v jednom řádku
col1, col2 = st.columns([4, 1])

with col1:
    st.title('FM Scouts app')

with col2:
    st.image('logo.jpg', width=80)

st.write('Select type of scatter plot to generate')

# import databáze

def load_db():
    return pd.read_excel('db.xlsx')

db = load_db()

# výběr ligy
league = st.selectbox("Select league:", sorted(db["league_name"].unique()))
filtered_league = db[db["league_name"] == league]

# výběr typu scatter plot
scatter_options = {
    "xG vs. Goals": ("xg", "goals"),
    "Shots on target vs. Goals": ("shots_on_target", "goals"),
    "xA vs. Assists": ("xa", "assists"),
    "Passes vs. Passes completed": ("passes", "passes_completed"),
    "Crosses vs. Accurate crosses": ("crosses", "accurate_crosses"),
    "Dribbles vs. Successful dribbles": ("dribbles", "dribbles_successful"),
    "Tackles vs. Interceptions": ("tackles", "interceptions"),
    "Duels vs. Duels Won": ("duels", "duels_won")
}

scatter_type = st.selectbox("Select scatter plot type:", list(scatter_options.keys()))

# tlačítko pro generování grafu
generate = st.button("Generate scatter plot")

# generování grafu
if generate:
    x_col, y_col = scatter_options[scatter_type]
    df = filtered_league.copy().dropna(subset=[x_col, y_col])

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(df[x_col], df[y_col], alpha=0.7)

    # lineární regrese
    m, b = np.polyfit(df[x_col], df[y_col], 1)
    x_vals = np.linspace(df[x_col].min(), df[x_col].max(), 100)
    ax.plot(x_vals, m * x_vals + b, color="red", linewidth=2, label="Regression line")

    # residua = rozdíl od regresní přímky
    df["residual"] = df[y_col] - (m * df[x_col] + b)

    # 5 největších overperformerů (nad čarou)
    top5 = df.sort_values("residual", ascending=False).head(5)

    # 5 největších underperformerů (pod čarou)
    bottom5 = df.sort_values("residual", ascending=True).head(5)

    # zaokrouhlení na 2 desetinná místa
    top5["residual"] = top5["residual"].round(2)
    bottom5["residual"] = bottom5["residual"].round(2)

    texts = []

    # overperformers
    for _, row in top5.iterrows():
        texts.append(
            ax.text(
                row[x_col] + random.uniform(-0.1, 0.1),
                row[y_col] + 0.3 + random.uniform(-0.1, 0.1),
                row["player_name"],
                fontsize=9,
                color="green",
                fontweight="bold"
            )
        )

    # underperformers
    for _, row in bottom5.iterrows():
        texts.append(
            ax.text(
                row[x_col] + random.uniform(-0.1, 0.1),
                row[y_col] - 0.3 + random.uniform(-0.1, 0.1),
                row["player_name"],
                fontsize=9,
                color="red",
                fontweight="bold"
            )
        )

    # automatické rozložení textů
    adjust_text(
        texts,
        ax=ax,
        arrowprops=dict(arrowstyle="-", color="gray", lw=0.5),
        force_text=0.7,
        force_points=0.5,
        expand_text=(1.3, 1.5),
        expand_points=(1.3, 1.5),
        lim=200
    )

    # legenda
    over_handle = ax.scatter([], [], color="green", label="Overperformers")
    under_handle = ax.scatter([], [], color="red", label="Underperformers")

    ax.legend()

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{scatter_type} – {league}")
    ax.legend()

    st.pyplot(fig)

    st.subheader("Top 5 overperformers")
    st.dataframe(
        top5[[ "player_name", x_col, y_col, "residual" ]].rename(
            columns={
                "player_name": "Player",
                x_col: x_col.upper(),
                y_col: y_col.upper(),
                "residual": "Overperformance"
            }
        )
    )

    st.subheader("Top 5 underperformers")
    st.dataframe(
        bottom5[[ "player_name", x_col, y_col, "residual" ]].rename(
            columns={
                "player_name": "Player",
                x_col: x_col.upper(),
                y_col: y_col.upper(),
                "residual": "Underperformance"
            }
        )
    )