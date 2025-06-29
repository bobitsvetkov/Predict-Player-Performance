import streamlit as st
import pandas as pd
import plotly.express as px


def show_training_result():
    df = pd.read_json("player_data.json")

    st.title("Player Scores and Tiers Dashboard")

    tier_filter = st.multiselect(
        "Select Tiers to display",
        options=df["Tier"].unique(),
        default=df["Tier"].unique(),
    )

    filtered_df = df[df["Tier"].isin(tier_filter)]

    score_type = "Predicted_Score"

    color_map = {
        "Champion": "#FFD700",
        "Good Player": "#1E90FF",
        "Above Average": "#32CD32",
        "Average": "#FFA500",
        "Below Average": "#FF6347",
        "New Player": "#A9A9A9",
    }

    fig = px.scatter(
        filtered_df,
        x=score_type,
        y="K/D ratio",
        color="Tier",
        color_discrete_map=color_map,
        hover_data=["Player", "Win %", "Chevrons/game", "Playoff Rate"],
        title=f"{score_type} vs K/D Ratio by Player Tier",
    )

    st.plotly_chart(fig)

    columns_to_show = [
        "Player",
        "Tier",
        "Win %",
        "K/D ratio",
        "Chevrons/game",
        "Playoff Rate",
        score_type,
    ]

    df_display = (
        filtered_df[columns_to_show]
        .sort_values(by=score_type, ascending=False)
        .reset_index(drop=True)
    )
    df_display.index += 1
    df_display.index.name = "Rank"

    st.dataframe(df_display)
