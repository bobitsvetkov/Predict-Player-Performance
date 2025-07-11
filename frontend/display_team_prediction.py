import streamlit as st
import pandas as pd
import plotly.express as px
import json


@st.cache_data
def load_teams(filename="data/team_tiers.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(
            f"Error: Data file '{filename}' not found. Please ensure it's in the correct location."
        )
        return []


def show_team_analysis():
    st.title("🏆 Team Tier & Placement Analysis")

    data = load_teams()

    if not data:
        return

    df = pd.json_normalize(data)

    df.rename(
        columns={
            "Team_Name": "team_name",
            "Tier": "tier",
            "Distance_From_Best": "distance_from_best",
            "Features.Elo_Rating": "elo_rating",
            "Features.Win_Rate": "win_rate",
            "Features.Total_Matches": "total_matches",
            "Rank_Within_Tier": "rank_within_tier",
            "Placement_Explanation": "placement_explanation",
            "Tier_Profile.Elo_Rating": "tier_elo_avg",
            "Tier_Profile.Win_Rate": "tier_win_avg",
            "Tier_Profile.Total_Matches": "tier_matches_avg",
            "Feature_Importance.Elo_Rating": "fi_elo_rating",
            "Feature_Importance.Win_Rate": "fi_win_rate",
            "Feature_Importance.Total_Matches": "fi_total_matches",
        },
        inplace=True,
    )

    df["elo_rating"] = df["elo_rating"].round(1)
    df["win_rate"] = df["win_rate"].round(1)
    df["total_matches"] = df["total_matches"].round(0)

    df["tier_elo_avg"] = df["tier_elo_avg"].round(1)
    df["tier_win_avg"] = df["tier_win_avg"].round(1)
    df["tier_matches_avg"] = df["tier_matches_avg"].round(0)

    ordered_tier_labels = [
        "Legendary",
        "Exceptional",
        "Advanced",
        "Skilled",
        "Intermediate",
        "Below Average",
        "Beginner",
    ]
    
    df["tier"] = pd.Categorical(
        df["tier"], categories=ordered_tier_labels, ordered=True
    )
    df.sort_values(by="tier", inplace=True)

    tier_colors = {
        "Legendary": "#FFD700",
        "Exceptional": "#8E5FBF",
        "Advanced": "#4099D1",
        "Skilled": "#4CA64C",
        "Intermediate": "#E39B2D",
        "Below Average": "#FF6347",
        "Beginner": "#B0B0B0",
    }

    min_matches = st.sidebar.slider(
        "Minimum matches played",
        int(df["total_matches"].min()),
        int(df["total_matches"].max()),
        1,
    )
    df_filtered = df[df["total_matches"] >= min_matches].copy()

    st.subheader("Summary Table")

    display_cols = ["team_name", "tier", "elo_rating", "win_rate"]
    df_display = df_filtered[display_cols].copy()
    df_display.rename(
        columns={
            "team_name": "Team Name",
            "tier": "Tier",
            "elo_rating": "ELO Rating",
            "win_rate": "Win Rate (%)",
        },
        inplace=True,
    )

    st.dataframe(
        df_display.style.format(
            {
                "ELO Rating": "{:.1f}",
                "Win Rate (%)": "{:.1f}",
            }
        ),
        use_container_width=True,
    )

    st.subheader("Individual Team Placement Details and Analysis")

    team_names = df_filtered["team_name"].unique()
    selected_team_name = st.selectbox(
        "Select a team for detailed analysis:",
        team_names,
        index=0,
    )

    if selected_team_name:
        selected_team_row = df_filtered[
            df_filtered["team_name"] == selected_team_name
        ].iloc[0]

        with st.expander(
            f"Detailed Analysis for {selected_team_row['team_name']} ({selected_team_row['tier']}-Tier)",
            expanded = True
        ):
            st.markdown(f"**Team Name:** {selected_team_row['team_name']}")
            st.markdown(f"**Assigned Tier:** {selected_team_row['tier']}")
            st.markdown(
                f"**Rank within {selected_team_row['tier']}-Tier:** {selected_team_row['rank_within_tier']}"
            )

            st.markdown("### Placement Explanation")
            st.markdown(selected_team_row["placement_explanation"])

            tier_avg_data = df[
                ["tier", "tier_elo_avg", "tier_win_avg", "tier_matches_avg"]
            ].drop_duplicates()
            tier_avg_data["tier"] = pd.Categorical(
                tier_avg_data["tier"], categories=ordered_tier_labels, ordered=True
            )
            tier_avg_data = tier_avg_data.sort_values("tier")


            st.markdown("#### Comparison vs Tier Average")
            selected_tier_avg = tier_avg_data[tier_avg_data["tier"] == selected_team_row["tier"]].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                elo_delta = round(selected_team_row['elo_rating'] - selected_tier_avg['tier_elo_avg'], 1)
                st.metric(
                    label="ELO Rating",
                    value=f"{selected_team_row['elo_rating']:.1f}",
                    delta=f"{elo_delta:+.1f}" if elo_delta != 0 else "0.0",
                    help=f"vs {selected_team_row['tier']}-Tier Average: {selected_tier_avg['tier_elo_avg']:.1f}"
                )
            
            with col2:
                win_rate_delta = round(selected_team_row['win_rate'] - selected_tier_avg['tier_win_avg'], 1)
                st.metric(
                    label="Win Rate (%)",
                    value=f"{selected_team_row['win_rate']:.1f}%",
                    delta=f"{win_rate_delta:+.1f}%" if win_rate_delta != 0 else "0.0%",
                    help=f"vs {selected_team_row['tier']}-Tier Average: {selected_tier_avg['tier_win_avg']:.1f}%"
                )
            
            with col3:
                matches_delta = round(selected_team_row['total_matches'] - selected_tier_avg['tier_matches_avg'], 0)
                st.metric(
                    label="Total Matches",
                    value=f"{selected_team_row['total_matches']:.0f}",
                    delta=f"{matches_delta:+.0f}" if matches_delta != 0 else "0",
                    help=f"vs {selected_team_row['tier']}-Tier Average: {selected_tier_avg['tier_matches_avg']:.0f}"
                )
            st.markdown("---")

    st.subheader("ELO Rating vs Win Rate Scatter Plot")

    fig_scatter = px.scatter(
        df_filtered,
        x="elo_rating",
        y="win_rate",
        color="tier",
        size="total_matches",
        color_discrete_map=tier_colors,
        hover_data={
            "team_name": True,
            "elo_rating": True,
            "win_rate": True,
            "total_matches": True,
        },
        labels={
            "elo_rating": "ELO Rating",
            "win_rate": "Win Rate (%)",
            "tier": "Tier",
            "total_matches": "Matches Played",
        },
        title="ELO Rating vs Win Rate by Tier (bubble size = matches played)",
    )

    fig_scatter.update_layout(height=600)
    st.plotly_chart(fig_scatter, use_container_width=True)