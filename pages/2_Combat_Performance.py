
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        plot_bgcolor="#172033",
        font=dict(color="#F8FAFC", size=13),
        margin=dict(l=20, r=20, t=65, b=35),
        height=400
    )
    return fig

st.set_page_config(
    page_title="Combat Performance",
    page_icon="🎯",
    layout="wide"
)

df = pd.read_csv(
    Path(__file__).resolve().parent.parent
    / "csgo_players_cleaned.csv"
)

st.title("🎯 Combat Performance Analysis")
st.caption("Historical CS:GO professional player statistics")

# Country filter
countries = st.sidebar.multiselect(
    "Select Countries",
    sorted(df["country"].unique())
)

if countries:
    df = df[df["country"].isin(countries)]

# Minimum maps filter
min_maps = st.sidebar.slider(
    "Minimum Maps Played",
    0,
    int(df["maps_played"].max()) if not df.empty else 0,
    100
    if not df.empty and df["maps_played"].max() >= 100
    else 0
)

df = df[df["maps_played"] >= min_maps]

if df.empty:
    st.warning("No players match the filters.")
    st.stop()

# KPI cards
c1, c2, c3, c4 = st.columns(4)

c1.metric("Players", len(df))
c2.metric("Average K/D", f"{df['kills_per_death'].mean():.2f}")
c3.metric("Average Damage/Round", f"{df['damage_per_round'].mean():.1f}")
c4.metric("Average Headshot %", f"{df['headshot_percentage'].mean():.1f}%")

st.divider()

# Row 1
left, right = st.columns(2)

with left:
    fig1 = px.scatter(
        df,
        x="total_kills",
        y="total_deaths",
        hover_name="nickname",
        hover_data=["rating", "maps_played"],
        title="Total Kills vs Total Deaths"
    )
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)


with right:
    fig2 = px.histogram(
        df,
        x="kills_per_death",
        title="K/D Ratio Distribution",
        labels={
            "kills_per_death": "K/D Ratio"
        },
        color_discrete_sequence=["#38BDF8"]
    )

    fig2.update_traces(
        xbins=dict(start=0.65, end=1.56, size=0.05),
        marker_line_color="#0B1120",
        marker_line_width=1
    )

    fig2.update_layout(
        bargap=0.08,
        yaxis_title="Number of Players",
        xaxis_title="K/D Ratio"
    )

    st.plotly_chart(style_chart(fig2), use_container_width=True)


# Row 2
left2, right2 = st.columns(2)

with left2:
    fig3 = px.scatter(
        df,
        x="damage_per_round",
        y="rating",
        hover_name="nickname",
        title="Damage per Round vs Rating"
    )
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

with right2:
    top_kd = df.nlargest(10, "kills_per_death")

    fig4 = px.bar(
        top_kd,
        x="nickname",
        y="kills_per_death",
        color="kills_per_death",
        color_continuous_scale="Blues",
        title="Top 10 Players by K/D Ratio"
    )
    fig4.update_layout(
        template="plotly_dark",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig4, use_container_width=True)

# Row 3
left3, right3 = st.columns(2)


with left3:
    fig5 = px.histogram(
        df,
        x="headshot_percentage",
        title="Headshot Percentage Distribution",
        color_discrete_sequence=["#38BDF8"]
    )

    fig5.update_traces(
        xbins=dict(start=0, end=101, size=5),
        marker_line_color="#0B1120",
        marker_line_width=1
    )

    fig5.update_layout(
        bargap=0.08,
        xaxis_title="Headshot Percentage (%)",
        yaxis_title="Number of Players"
    )

    st.plotly_chart(style_chart(fig5), use_container_width=True)


with right3:
    fig6 = px.scatter(
        df,
        x="opening_kill_ratio",
        y="rating",
        hover_name="nickname",
        title="Opening Kill Ratio vs Rating"
    )
    fig6.update_layout(template="plotly_dark")
    st.plotly_chart(fig6, use_container_width=True)
