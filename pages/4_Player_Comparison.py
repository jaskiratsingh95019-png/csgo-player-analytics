
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Player Comparison",
    page_icon="🏆",
    layout="wide"
)

df = pd.read_csv(
    Path(__file__).resolve().parent.parent
    / "csgo_players_cleaned.csv"
)

st.title("🏆 Professional Player Comparison")
st.caption("Compare historical CS:GO player statistics")

# Player selectors
names = sorted(df["nickname"].unique())

c1, c2 = st.columns(2)

with c1:
    player1 = st.selectbox(
        "Choose Player 1",
        names,
        index=names.index("ZywOo") if "ZywOo" in names else 0
    )

with c2:
    player2 = st.selectbox(
        "Choose Player 2",
        names,
        index=names.index("s1mple") if "s1mple" in names else 1
    )

if player1 == player2:
    st.warning("Select two different players.")
    st.stop()

p1 = df[df["nickname"] == player1].iloc[0]
p2 = df[df["nickname"] == player2].iloc[0]

# KPI cards
a, b, c, d = st.columns(4)

a.metric(f"{player1} Rating", f"{p1['rating']:.2f}")
b.metric(f"{player2} Rating", f"{p2['rating']:.2f}")
c.metric(f"{player1} K/D", f"{p1['kills_per_death']:.2f}")
d.metric(f"{player2} K/D", f"{p2['kills_per_death']:.2f}")

st.divider()

# Comparison table
stats = {
    "Rating": "rating",
    "K/D Ratio": "kills_per_death",
    "Damage / Round": "damage_per_round",
    "Kills / Round": "kills_per_round",
    "Headshot %": "headshot_percentage",
    "Maps Played": "maps_played"
}

comparison = pd.DataFrame({
    "Statistic": list(stats.keys()),
    player1: [p1[col] for col in stats.values()],
    player2: [p2[col] for col in stats.values()]
})

st.subheader("Player Statistics")
st.dataframe(comparison, hide_index=True, use_container_width=True)

left, right = st.columns(2)

# Chart 1: Player ratings
with left:
    rating_data = pd.DataFrame({
        "Player": [player1, player2],
        "Rating": [p1["rating"], p2["rating"]]
    })

    fig1 = px.bar(
        rating_data,
        x="Player",
        y="Rating",
        title="Player Rating Comparison",
        color="Player"
    )
    fig1.update_layout(template="plotly_dark", showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Damage per round
with right:
    damage_data = pd.DataFrame({
        "Player": [player1, player2],
        "Damage / Round": [
            p1["damage_per_round"],
            p2["damage_per_round"]
        ]
    })

    fig2 = px.bar(
        damage_data,
        x="Player",
        y="Damage / Round",
        title="Damage per Round Comparison",
        color="Player"
    )
    fig2.update_layout(template="plotly_dark", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: K/D comparison
st.subheader("K/D Performance")

kd_data = pd.DataFrame({
    "Player": [player1, player2],
    "K/D Ratio": [
        p1["kills_per_death"],
        p2["kills_per_death"]
    ]
})

fig3 = px.bar(
    kd_data,
    x="Player",
    y="K/D Ratio",
    color="Player",
    title="K/D Ratio Comparison"
)
fig3.update_layout(template="plotly_dark", showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Statistical correlation heatmap
st.subheader("Performance Correlation")

numeric_columns = [
    "rating",
    "kills_per_death",
    "damage_per_round",
    "kills_per_round",
    "headshot_percentage"
]

correlation = df[numeric_columns].corr()

fig4 = px.imshow(
    correlation,
    text_auto=".2f",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
    title="Player Performance Correlation Heatmap"
)
fig4.update_layout(template="plotly_dark")
st.plotly_chart(fig4, use_container_width=True)
