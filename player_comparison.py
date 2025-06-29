import streamlit as st
import pandas as pd
from utils import compute_percentiles, percent_str_to_float


def compare_stat(val1, val2, percentile1, percentile2):
    if percentile1 > percentile2:
        color = "green"
        arrow = "▲"
    elif percentile1 < percentile2:
        color = "red"
        arrow = "▼"
    else:
        color = "gray"
        arrow = "→"
    perc_diff = (percentile1 - percentile2) * 100
    sign = "+" if perc_diff > 0 else ""
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

    percentiles = compute_percentiles(df, features)

    st.title("Player Comparison")

    player1 = st.selectbox("Select Player 1", df["Player"].unique())
    player2 = st.selectbox("Select Player 2", df["Player"].unique())

    if player1 == player2:
        st.warning("Please select two different players.")
        return

    p1 = df[df["Player"] == player1].iloc[0]
    p2 = df[df["Player"] == player2].iloc[0]

    rows = []
    for feature in features:
        val1 = p1[feature]
        val2 = p2[feature]

        if feature in ["Win %", "Playoff Rate"]:
            val1_disp = p1[feature]
            val2_disp = p2[feature]
            perc1 = percent_str_to_float(p1[feature])
            perc2 = percent_str_to_float(p2[feature])
        else:
            val1_disp = f"{val1:.2f}"
            val2_disp = f"{val2:.2f}"
            perc1 = percentiles[feature].loc[p1.name]
            perc2 = percentiles[feature].loc[p2.name]

        comparison_html = compare_stat(val1, val2, perc1, perc2)

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
