import streamlit as st
import pandas as pd
import json


@st.cache_data
def load_teams(filename="data/team_tiers.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return pd.json_normalize(data)
    except FileNotFoundError:
        st.error(f"Error: Data file '{filename}' not found.")
        return pd.DataFrame()


def show_team_comparison():
    st.title("⚔️ Team vs Team Comparison")

    df = load_teams()
    if df.empty:
        return

    df.rename(
        columns={
            "Team_Name": "team_name",
            "Features.Elo_Rating": "elo_rating",
            "Features.Win_Rate": "win_rate",
            "Features.Total_Matches": "total_matches",
            "Tier": "tier",
        },
        inplace=True,
    )

    df["elo_rating"] = df["elo_rating"].round(1)
    df["win_rate"] = df["win_rate"].round(1)
    df["total_matches"] = df["total_matches"].astype(int)

    team_options = df["team_name"].unique()

    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Select Team 1", team_options)
    with col2:
        team2 = st.selectbox(
            "Select Team 2", team_options, index=1 if len(team_options) > 1 else 0
        )

    if team1 == team2:
        st.warning("Please select two different teams.")
        return

    team1_data = df[df["team_name"] == team1].iloc[0]
    team2_data = df[df["team_name"] == team2].iloc[0]

    stat_names = ["ELO Rating", "Win Rate (%)", "Total Matches"]
    stat_keys = ["elo_rating", "win_rate", "total_matches"]

    team1_wins = 0
    team2_wins = 0

    for label, key in zip(stat_names, stat_keys):
        val1 = team1_data[key]
        val2 = team2_data[key]
        delta = round(val1 - val2, 1 if key != "total_matches" else 0)

        if val1 > val2:
            team1_wins += 1
        elif val2 > val1:
            team2_wins += 1

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"{label} ({team1})", value=val1, delta=f"{delta:+}")
        with col2:
            st.metric(label=f"{label} ({team2})", value=val2, delta=f"{-delta:+}")
