import streamlit as st
import pandas as pd
from utils import percent_str_to_float


def compare_stat(val1, val2, is_percentage=False, epsilon=0.1):
    if is_percentage:
        diff = val1 - val2
        if abs(diff) < epsilon:
            diff = 0
        sign = "+" if diff > 0 else ""
        arrow = "▲" if diff > 0 else ("▼" if diff < 0 else "→")
        color = "green" if diff > 0 else ("red" if diff < 0 else "gray")
        return f'<span style="color:{color}">{arrow} {sign}{diff:.1f}%</span>'
    else:
        # For ratios or raw numbers, do relative percentage difference:
        if val2 == 0:
            perc_diff = 0
        else:
            perc_diff = ((val1 - val2) / val2) * 100
        if abs(perc_diff) < epsilon:
            perc_diff = 0
        sign = "+" if perc_diff > 0 else ""
        arrow = "▲" if perc_diff > 0 else ("▼" if perc_diff < 0 else "→")
        color = "green" if perc_diff > 0 else ("red" if perc_diff < 0 else "gray")
        return f'<span style="color:{color}">{arrow} {sign}{perc_diff:.1f}%</span>'


def show_player_comparison():
    df = pd.read_json("player_data.json")

    features = [
        "K/D ratio",
        "Chevrons/game",
        "Win %",
        "Playoff Rate",
        "Battle_Performance",
    ]

    st.title("Player Comparison")

    player1 = st.selectbox("Select Player 1", df["Player"].unique())
    player2 = st.selectbox("Select Player 2", df["Player"].unique())

    if player1 == player2:
        st.warning("Please select two different players.")
        return

    p1 = df[df["Player"] == player1].iloc[0]
    p2 = df[df["Player"] == player2].iloc[0]

    rows = []
    percentage_features = ["Win %", "Playoff Rate", "Battle_Performance"]

    for feature in features:
        val1 = p1[feature]
        val2 = p2[feature]
        if feature in percentage_features:
            val1_float = round(percent_str_to_float(val1), 2)
            val2_float = round(percent_str_to_float(val2), 2)
            val1_disp = f"{val1_float:.1f}%"
            val2_disp = f"{val2_float:.1f}%"
            comparison_html = compare_stat(val1_float, val2_float, is_percentage=True)
        else:
            val1_float = round(float(val1), 2)
            val2_float = round(float(val2), 2)
            val1_disp = f"{val1_float:.2f}"
            val2_disp = f"{val2_float:.2f}"
            comparison_html = compare_stat(val1_float, val2_float, is_percentage=False)

        rows.append(
            {
                "Statistic": feature,
                player1: val1_disp,
                player2: val2_disp,
                "Comparison": comparison_html,
            }
        )

    comp_df = pd.DataFrame(rows)

    st.write(f"### Comparing {player1} vs {player2}")
    st.write(comp_df.to_html(escape=False, index=False), unsafe_allow_html=True)
