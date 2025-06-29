import streamlit as st
from training_result import show_training_result
from player_comparison import show_player_comparison

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Training Results", "Player Comparison"])

if page == "Training Results":
    show_training_result()
elif page == "Player Comparison":
    show_player_comparison()
