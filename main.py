import streamlit as st
import pandas as pd
import plotly.express as px
from utils import format_decimal_to_percent

df = pd.read_json("player_data.json")

df["Win %"] = df["Win %"].apply(format_decimal_to_percent)

st.title("Player Scores and Tiers Dashboard")

tier_filter = st.multiselect(
    "Select Tiers to display",
    options=df["Tier"].unique(),
    default=df["Tier"].unique(),
)

filtered_df = df[df["Tier"].isin(tier_filter)]

score_type = "Predicted_Score"

fig = px.scatter(
    filtered_df,
    x=score_type,
    y="K/D ratio",
    color="Tier",
    hover_data=["Player", "Win %", "Chevrons/game", "Playoff Appearances"],
    title=f"{score_type} vs K/D Ratio by Player Tier",
)

st.plotly_chart(fig)

st.dataframe(
    filtered_df[
        ["Player", "Tier", "Win %", "K/D ratio", "Chevrons/game", score_type]
    ].sort_values(by=score_type, ascending=False)
)
