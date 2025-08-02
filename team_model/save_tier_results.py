import json
from typing import List, Dict, Any


def save_tier_results(results: List[Dict[str, Any]], output_file: str):
    if results is None:
        print("Error: Cannot save results - results is None")
        return

    if not results:
        print("Warning: Results list is empty")
        return

    clean_results = []
    for team in results:
        clean_team = {
            "Team_Name": team["Team_Name"],
            "Tier": team["Tier"],
            "Distance_From_Best": team["Distance_From_Best"],
            "Features": team["Features"],
            "Rank_Within_Tier": team["Rank_Within_Tier"],
            "Placement_Analysis": team.get("Placement_Analysis", "No analysis available"),
            "Placement_Explanation": team.get("Placement_Explanation", "No explanation available"),
            "Tier_Profile": team.get("Tier_Profile", {}),
            "Feature_Importance": team.get("Feature_Importance", {}),
        }
        clean_results.append(clean_team)

    with open(output_file, "w") as f:
        json.dump(clean_results, f, indent=2)

    print(f"Successfully saved {len(clean_results)} teams to {output_file}")


def print_tier_summary(results: List[Dict[str, Any]]):
    """Print a formatted tier summary"""
    if not results:
        print("No results to display")
        return
        
    print("\n=== TEAM TIER RANKINGS ===")
    
    if results and "Feature_Importance" in results[0]:
        print("\n=== FEATURE IMPORTANCE ===")
        feature_importance = results[0]["Feature_Importance"]
        for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
            feature_name = feature.replace("_", " ").title()
            print(f"{feature_name}: {importance*100:.1f}%")
    
    print("\n=== TIER PROFILES (Average Values) ===")
    tier_profiles = {}
    for team in results:
        tier = team["Tier"]
        if tier not in tier_profiles and "Tier_Profile" in team:
            tier_profiles[tier] = team["Tier_Profile"]
    
    tier_order = ["Legendary", "Exceptional", "Advanced", "Skilled", "Intermediate", "Below Average", "Beginner"]
    for tier in tier_order:
        if tier in tier_profiles:
            profile = tier_profiles[tier]
            print(f"{tier}-Tier: Elo={profile.get('Elo_Rating', 0):.1f}, "
                  f"Win Rate={profile.get('Win_Rate', 0)*100:.1f}%, "
                  f"Matches={profile.get('Total_Matches', 0):.1f}")

    tiers = {}
    for team in results:
        tier = team["Tier"]
        if tier not in tiers:
            tiers[tier] = []
        tiers[tier].append(team)