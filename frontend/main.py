import streamlit as st
from display_player_prediction import display_player_prediction
from player_comparison import show_player_comparison
from display_team_prediction import show_team_analysis
from team_comparison import show_team_comparison

st.set_page_config(
    page_title="Total War Prediction",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Navigation")

pages = {
    "Player Prediction": display_player_prediction,
    "Player Comparison": show_player_comparison,
    "Team Prediction": show_team_analysis,
    "Team Comparison": show_team_comparison,
}

page = st.sidebar.selectbox("Choose a page", list(pages.keys()))
pages[page]()