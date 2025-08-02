import streamlit as st
import pandas as pd
import plotly.express as px

def display_player_prediction():
    df = pd.read_json("data/player_data.json")

    st.title("Player Scores and Tiers Dashboard")

    score_type = "Predicted_Score"

    color_map = {
        "S": "#FFD700",
        "A": "#8E5FBF",
        "B": "#4099D1",
        "C": "#4CA64C",
        "D": "#E39B2D",
        "E": "#FF6347",
        "F": "#B0B0B0",
    }

    fig = px.scatter(
        df,
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
        df[columns_to_show]
        .sort_values(by=score_type, ascending=False)
        .reset_index(drop=True)
    )

    df_display.index += 1
    df_display.index.name = "Rank"

    df_display = df_display.style.format(
        {
            "Win %": "{:.2f}",
            "K/D ratio": "{:.2f}",
            "Chevrons/game": "{:.2f}",
            "Playoff Rate": "{:.2f}",
            score_type: "{:.2f}",
        }
    )

    st.dataframe(df_display)
