import streamlit as st
from display_player_prediction import display_player_prediction
from player_comparison import show_player_comparison
from tier_list import show_team_tier_list
from display_team_prediction import show_team_analysis

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["Player Prediction", "Player Comparison", "Team Tier List", "Team Prediction"],
)

if page == "Player Prediction":
    display_player_prediction()
elif page == "Player Comparison":
    show_player_comparison()
elif page == "Team Tier List":
    show_team_tier_list()
elif page == "Team Prediction":
    show_team_analysis()
