
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Weapon Analysis",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv(
    Path(__file__).resolve().parent.parent
    / "csgo_players_cleaned.csv"
)

st.title("📊 Weapon and Playstyle Analysis")
st.caption("Historical CS:GO professional player statistics")

# Sidebar filters
countries = st.sidebar.multiselect(
    "Select Countries",
    sorted(df["country"].unique())
)

min_maps = st.sidebar.slider(
    "Minimum Maps Played", 0,
    int(df["maps_played"].max()), 100
)

if countries:
    df = df[df["country"].isin(countries)]

df = df[df["maps_played"] >= min_maps].copy()

if df.empty:
    st.warning("No players match your filters.")
    st.stop()

weapons = {
    "Rifle": "rifle_kills",
    "Sniper": "sniper_kills",
    "SMG": "smg_kills",
    "Pistol": "pistol_kills",
    "Grenade": "grenade_kills",
    "Other": "other_kills"
}

# KPI cards
a, b, c, d = st.columns(4)

a.metric("Players", len(df))
b.metric("Rifle Kills", f"{df['rifle_kills'].sum():,}")
c.metric("Sniper Kills", f"{df['sniper_kills'].sum():,}")
d.metric("Pistol Kills", f"{df['pistol_kills'].sum():,}")

st.divider()

left, right = st.columns(2)

# Chart 1: Overall weapon distribution
with left:
    weapon_totals = pd.DataFrame({
        "Weapon": list(weapons.keys()),
        "Kills": [df[col].sum() for col in weapons.values()]
    })

    fig1 = px.pie(
        weapon_totals,
        names="Weapon",
        values="Kills",
        hole=0.5,
        title="Weapon Kill Distribution"
    )
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Top sniper players
with right:
    top = df.nlargest(10, "sniper_kills")

    fig2 = px.bar(
        top,
        x="nickname",
        y="sniper_kills",
        title="Top 10 Players by Sniper Kills",
        color_discrete_sequence=["#38BDF8"]
    )
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

left2, right2 = st.columns(2)

# Chart 3: Rifle versus sniper kills
with left2:
    fig3 = px.scatter(
        df,
        x="rifle_kills",
        y="sniper_kills",
        hover_name="nickname",
        hover_data=["maps_played", "rating"],
        title="Rifle Kills vs Sniper Kills"
    )
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Selected player weapon profile
with right2:
    player = st.selectbox(
        "Select a player",
        sorted(df["nickname"].unique())
    )

    selected = df[df["nickname"] == player].iloc[0]

    profile = pd.DataFrame({
        "Weapon": list(weapons.keys()),
        "Kills": [selected[col] for col in weapons.values()]
    })

    fig4 = px.bar(
        profile,
        x="Weapon",
        y="Kills",
        title=f"{player} - Weapon Profile",
        color_discrete_sequence=["#38BDF8"]
    )
    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)
