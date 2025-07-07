import streamlit as st
import pandas as pd
import plotly.express as px
import json


def load_elo_data():
    """Load ELO predictions data from JSON file"""
    try:
        with open("data/elo_skill_predictions.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(
            "ELO predictions file not found. Please run the ELO prediction model first."
        )
        return None
    except json.JSONDecodeError:
        st.error("Error reading ELO predictions file. Please check the file format.")
        return None


def show_elo_statistics(elo_stats, df):
    """Display ELO statistics in the sidebar"""
    st.sidebar.header("📊 Elo Statistics")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.metric("Total Teams", elo_stats["total_teams"])
        st.metric("Average ELO", f"{elo_stats['avg_elo']:.1f}")
        st.metric("Median ELO", f"{elo_stats['median_elo']:.1f}")
        st.metric("Average Win Rate", f"{df['win_rate'].mean():.1f}%")

    with col2:
        st.metric("Min ELO", f"{elo_stats['min_elo']:.1f}")
        st.metric("Max ELO", f"{elo_stats['max_elo']:.1f}")
        st.metric("ELO Range", f"{elo_stats['elo_range']:.1f}")
        st.metric("Average Matches", f"{df['total_matches'].mean():.1f}")

    st.sidebar.metric("Standard Deviation", f"{elo_stats['std_elo']:.1f}")


def show_team_analysis():
    """Main function to display team analysis dashboard"""
    st.title("🎯 Team Skill Prediction Dashboard")

    data = load_elo_data()
    if data is None:
        return

    df = pd.DataFrame(data["team_predictions"])

    show_elo_statistics(data["elo_statistics"], df)

    st.header("🔍 Game Filter")

    min_matches = st.slider(
        "Minimum number of matches",
        min_value=int(df["total_matches"].min()),
        max_value=int(df["total_matches"].max()),
        value=int(df["total_matches"].min()),
        step=1,
    )

    filtered_df = df[(df["total_matches"] >= min_matches)]

    color_map = {
        "Beginner": "#B0B0B0",
        "Below Average": "#FF6347",
        "Intermediate": "#E39B2D",
        "Skilled": "#4CA64C",
        "Advanced": "#4099D1",
        "Exceptional": "#8E5FBF",
        "Legendary": "#FFD700",
    }

    st.subheader("📋 Team Rankings")

    columns_to_show = [
        "team_name",
        "skill_level",
        "elo_ranking",
        "elo_rating",
        "win_rate",
        "total_matches",
        "percentile",
    ]

    df_display = filtered_df[columns_to_show].reset_index(drop=True)

    df_display.columns = [
        "Team Name",
        "Skill Level",
        "ELO Rank",
        "ELO Rating",
        "Win Rate (%)",
        "Total Matches",
        "Percentile",
    ]

    df_display.index += 1
    df_display.index.name = "Display Rank"

    def highlight_skill_level(row):
        color = color_map.get(row["Skill Level"], "#FFFFFF")
        return [f"background-color: {color}; opacity: 0.3"] * len(row)

    styled_df = df_display.style.apply(highlight_skill_level, axis=1).format(
        {
            "ELO Rating": "{:.2f}",
            "Win Rate (%)": "{:.2f}",
            "Percentile": "{:.2f}",
        }
    )

    st.dataframe(styled_df, use_container_width=True)

    st.subheader("📈 ELO Rating vs Win Rate by Skill Level")

    fig_scatter = px.scatter(
        filtered_df,
        x="elo_rating",
        y="win_rate",
        color="skill_level",
        color_discrete_map=color_map,
        size="total_matches",
        hover_data={
            "team_name": True,
            "elo_ranking": True,
            "percentile": True,
            "total_matches": True,
            "elo_rating": ":.1f",
            "win_rate": ":.1f",
        },
        title="ELO Rating vs Win Rate (bubble size = total matches)",
        labels={
            "elo_rating": "ELO Rating",
            "win_rate": "Win Rate (%)",
            "skill_level": "Skill Level",
        },
    )

    fig_scatter.update_layout(
        xaxis_title="ELO Rating", yaxis_title="Win Rate (%)", height=600
    )

    st.plotly_chart(fig_scatter, use_container_width=True)


if __name__ == "__main__":
    show_team_analysis()
