import streamlit as st
import json

def show_team_tier_list():
    with open("outputs/team_tiers.json") as f:
        tiered_teams = json.load(f)

    tiers = {}
    for team in tiered_teams:
        tier = team["Tier"]
        tiers.setdefault(tier, []).append(team)

    tier_order = ["S", "A", "B", "C", "D", "E", "F"]
    tier_labels = {
        "S": "🔥 Tier S",
        "A": "💪 Tier A",
        "B": "⚔️ Tier B",
        "C": "🛡️ Tier C",
        "D": "🪶 Tier D",
        "E": "🛡️ Tier E",
        "F": "💤 Tier F"
    }

    st.title("🏆 Total War Team Tier List")

    for tier in tier_order:
        if tier not in tiers:
            continue
        st.markdown(f"## {tier_labels[tier]}")
        teams = sorted(tiers[tier], key=lambda x: x.get("Rank_Within_Tier", 999))

        with st.expander(f"Show {len(teams)} teams in {tier_labels[tier]}"):
            for team in teams:
                with st.container():
                    st.markdown(f"**#{team['Rank_Within_Tier']} - {team['Team_Name']}**")
                    st.markdown(
                        f"- Elo: `{team['Features']['Elo_Rating']}` &nbsp;&nbsp;| "
                        f"Win Rate: `{team['Features']['Win_Rate']}%` &nbsp;&nbsp;| "
                        f"Matches: `{team['Features']['Total_Matches']}`"
                    )

                    with st.expander("📊 Placement Explanation"):
                        st.markdown(team.get("Placement_Explanation", "No explanation available."))

                    with st.expander("🧠 Placement Analysis"):
                        st.markdown(team.get("Placement_Analysis", "No analysis available."))

                    st.markdown("---")

if __name__ == "__main__":
    show_team_tier_list()
