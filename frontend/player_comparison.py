import streamlit as st
import pandas as pd
import numpy as np


def percent_str_to_float(s):
    if isinstance(s, str) and s.endswith("%"):
        return float(s.strip("%"))
    elif pd.isnull(s):
        return np.nan
    else:
        return float(s)


def show_player_comparison():
    st.title("Player vs Player Comparison")

    df = pd.read_json("data/player_data.json")

    features = [
        "K/D ratio",
        "Chevrons/game",
        "Win %",
        "Playoff Rate",
        "Battle_Performance",
    ]

    percentage_features = {"Win %", "Playoff Rate", "Battle_Performance"}

    player_options = df["Player"].unique()

    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("Select Player 1", player_options)
    with col2:
        player2 = st.selectbox(
            "Select Player 2",
            player_options,
            index=1 if len(player_options) > 1 else 0,
        )

    if player1 == player2:
        st.warning("Please select two different players.")
        return

    p1 = df[df["Player"] == player1].iloc[0]
    p2 = df[df["Player"] == player2].iloc[0]

    p1_wins = 0
    p2_wins = 0

    st.markdown(f"### Comparing **{player1}** vs **{player2}**")

    for feature in features:
        col1, col2 = st.columns(2)

        is_percentage = feature in percentage_features

        if is_percentage:
            val1 = round(percent_str_to_float(p1[feature]), 1)
            val2 = round(percent_str_to_float(p2[feature]), 1)
            unit = "%"
        else:
            val1 = round(float(p1[feature]), 2)
            val2 = round(float(p2[feature]), 2)
            unit = ""

        delta = round(val1 - val2, 1 if is_percentage else 2)

        if val1 > val2:
            p1_wins += 1
        elif val2 > val1:
            p2_wins += 1

        with col1:
            st.metric(
                label=f"{feature} ({player1})",
                value=f"{val1}{unit}",
                delta=f"{delta:+}{unit}" if delta != 0 else "0",
                delta_color="normal",
            )
        with col2:
            st.metric(
                label=f"{feature} ({player2})",
                value=f"{val2}{unit}",
                delta=f"{-delta:+}{unit}" if delta != 0 else "0",
                delta_color="normal",
            )

    st.markdown("---")
    if p1_wins != p2_wins:
        winner = player1 if p1_wins > p2_wins else player2
        st.success(f"🏆 **{winner} wins the comparison!**")
    else:
        st.info("⚖️ It's a tie!")
