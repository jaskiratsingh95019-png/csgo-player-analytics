
import streamlit as st
import pandas as pd

# Configure the dashboard
st.set_page_config(
    page_title="CS:GO Player Analytics",
    page_icon="🎮",
    layout="wide"
)

# Load our cleaned dataset
df = pd.read_csv("csgo_players_cleaned.csv")

# Sidebar filters
st.sidebar.title("🎮 Player Filters")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df["country"].unique()),
    default=[]
)

if selected_countries:
    filtered_df = df[
        df["country"].isin(selected_countries)
    ].copy()
else:
    filtered_df = df.copy()

# Top 10 players from selected countries
top_10 = filtered_df.nlargest(10, "rating")


# Dashboard heading
st.title("🎮 CS:GO Professional Player Analytics")
st.write("Historical Professional Player Performance Dashboard")

# Create KPI cards
col1, col2, col3, col4 = st.columns(4)


# Create KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Players", len(filtered_df))

with col2:
    st.metric("Countries", filtered_df["country"].nunique())

with col3:
    st.metric("Average Rating", round(filtered_df["rating"].mean(), 2))

with col4:
    st.metric("Average K/D", round(filtered_df["kills_per_death"].mean(), 2))

st.subheader("Player Dataset Preview")

# Display first 10 players with numbering from 1
preview_df = filtered_df.head(10).copy()

preview_df.index = range(1, len(preview_df) + 1)

st.dataframe(preview_df, use_container_width=True)

import plotly.express as px

# Custom dashboard styling
st.markdown("""
<style>
.stApp {
    background-color: #0B1120;
    color: #F8FAFC;
}

[data-testid="stMetric"] {
    background: #172033;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #334155;
}

[data-testid="stMetricValue"] {
    color: #38BDF8;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}
</style>
""", unsafe_allow_html=True)

st.divider()

st.subheader("🏆 Top 10 Professional Players")

# Get the highest-rated players
top_10 = df.nlargest(10, "rating")

fig = px.bar(
    top_10,
    x="nickname",
    y="rating",
    color="rating",
    color_continuous_scale="Blues",
    hover_data=["country", "kills_per_death", "maps_played"],
    title="Top 10 CS:GO Players by Rating"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0B1120",
    plot_bgcolor="#172033",
    font_color="white",
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)



# ----------------------------------------
# PLAYER DEMOGRAPHICS
# ----------------------------------------

st.divider()
st.subheader("🌍 Player Demographics")

chart1, chart2 = st.columns(2)

# Chart 1: Top 10 countries
with chart1:
    country_counts = (
        filtered_df["country"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country_counts.columns = ["Country", "Players"]

    fig_country = px.bar(
        country_counts,
        x="Players",
        y="Country",
        orientation="h",
        title="Top 10 Countries by Player Count",
        color="Players",
        color_continuous_scale="Blues"
    )

    fig_country.update_yaxes(categoryorder="total ascending")
    fig_country.update_layout(
        template="plotly_dark",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_country, use_container_width=True)


# Chart 2: Age distribution
with chart2:
    age_counts = (
        filtered_df["age"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_counts.columns = ["Age", "Players"]

    fig_age = px.bar(
        age_counts,
        x="Age",
        y="Players",
        title="Professional Player Age Distribution",
        color_discrete_sequence=["#38BDF8"],
        text="Players"
    )

    fig_age.update_layout(
        template="plotly_dark",
        xaxis_title="Player Age",
        yaxis_title="Number of Players",
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        yaxis=dict(
            tickformat="d"
        )
    )

    st.plotly_chart(fig_age, use_container_width=True)


# ----------------------------------------
# RATING AND TEAM ANALYSIS
# ----------------------------------------

st.divider()
st.subheader("📊 Rating and Team Analysis")

chart3, chart4 = st.columns(2)


# Chart 3: Rating distribution
with chart3:
    fig_rating = px.histogram(
        filtered_df,
        x="rating",
        title="Player Rating Distribution",
        color_discrete_sequence=["#38BDF8"]
    )

    fig_rating.update_traces(
        xbins=dict(start=0.7, end=1.41, size=0.05),
        marker_line_color="#0B1120",
        marker_line_width=1,
        texttemplate="%{y}",
        textposition="outside"
    )

    fig_rating.update_layout(
        template="plotly_dark",
        xaxis_title="Player Rating",
        yaxis_title="Number of Players",
        bargap=0.08,
        yaxis=dict(tickformat="d")
    )

    st.plotly_chart(fig_rating, use_container_width=True)


# Chart 4: Top 10 recorded teams
with chart4:
    team_counts = (
        filtered_df[
            filtered_df["current_team"] != "Unknown"
        ]["current_team"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    team_counts.columns = ["Team", "Players"]

    fig_teams = px.bar(
        team_counts,
        x="Players",
        y="Team",
        orientation="h",
        title="Top 10 Teams by Recorded Player Count",
        color="Players",
        color_continuous_scale="Blues"
    )

    fig_teams.update_yaxes(categoryorder="total ascending")
    fig_teams.update_layout(
        template="plotly_dark",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_teams, use_container_width=True)
