import streamlit as st
from display_player_prediction import display_player_prediction
from player_comparison import show_player_comparison
from display_team_prediction import show_team_analysis
from team_comparison import show_team_comparison

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    [
        "Player Prediction",
        "Player Comparison",
        "Team Tier List",
        "Team Prediction",
        "Team Comparison",
    ],
)

if page == "Player Prediction":
    display_player_prediction()
elif page == "Player Comparison":
    show_player_comparison()
elif page == "Team Prediction":
    show_team_analysis()
elif page == "Team Comparison":
    show_team_comparison()
