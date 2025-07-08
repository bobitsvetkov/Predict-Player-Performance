import numpy as np
from typing import List, Dict, Any
from sklearn.preprocessing import StandardScaler
from clustering import calculate_feature_importance, calculate_distance_from_best_cluster


def generate_placement_explanation(
    team: Dict[str, Any], 
    tier_profile: Dict[str, float], 
    feature_importance: Dict[str, float],
    team_vector: np.ndarray,
    cluster_center: np.ndarray,
    assigned_tier: str
) -> str:
    """Generate detailed explanation for why a team is in a specific tier"""
    
    explanations = []
    tier = assigned_tier
    
    feature_map = {
        "Elo_Rating": ("Elo Rating", team["Elo_Rating"]),
        "Win_Rate": ("Win Rate", team["Win_Rate"]),
        "Total_Matches": ("Total Matches", team["Total_Matches"])
    }
    
    feature_contributions = []
    
    for i, (feature_key, (feature_name, team_value)) in enumerate(feature_map.items()):
        tier_average = tier_profile.get(feature_key, 0)
        importance = feature_importance.get(feature_key, 0)
        
        if feature_key == "Win_Rate":
            tier_average_pct = tier_average
            difference = team_value - tier_average_pct
            comparison = f"vs tier avg {tier_average_pct:.1f}%"
        else:
            difference = team_value - tier_average
            comparison = f"vs tier avg {tier_average:.1f}"
        
        if abs(difference) > 0.1:
            direction = "above" if difference > 0 else "below"
            strength = "significantly" if abs(difference) > (tier_average * 0.2) else "slightly"
            
            feature_contributions.append({
                "feature": feature_name,
                "value": team_value,
                "tier_avg": tier_average,
                "difference": difference,
                "direction": direction,
                "strength": strength,
                "importance": importance,
                "comparison": comparison
            })
    
    feature_contributions.sort(key=lambda x: x["importance"], reverse=True)
    
    explanations.append(f"Placed in {tier} tier based on:")
    
    for contrib in feature_contributions:
        importance_pct = contrib["importance"] * 100
        explanations.append(
            f"• {contrib['feature']}: {contrib['value']:.1f} ({contrib['comparison']}) - "
            f"{contrib['strength']} {contrib['direction']} tier average "
            f"[{importance_pct:.1f}% importance]"
        )
    
    total_distance = np.linalg.norm(team_vector - cluster_center)
    if total_distance < 0.5:
        explanations.append(f"• Strong fit for {tier} tier (distance: {total_distance:.2f})")
    elif total_distance > 1.5:
        explanations.append(f"• Borderline case for {tier} tier (distance: {total_distance:.2f})")
    else:
        explanations.append(f"• Good fit for {tier} tier (distance: {total_distance:.2f})")
    
    return " ".join(explanations)


def assign_tiers_and_rank_teams(
    team_features: List[Dict[str, Any]],
    X_scaled: np.ndarray,
    labels: np.ndarray,
    cluster_centers_scaled: np.ndarray,
    scaler: StandardScaler,
    feature_columns: List[str],
) -> List[Dict[str, Any]]:
    """Assign tiers (Legendary, Exceptional, Advanced, Skilled, Intermediate, Below Average, Beginner) and rank teams based on learned cluster patterns"""

    # Convert cluster centers back to original scale
    cluster_centers_original = scaler.inverse_transform(cluster_centers_scaled)

    feature_importance = calculate_feature_importance(cluster_centers_original, feature_columns)
    
    cluster_strengths = []
    cluster_profiles = {}
    
    for i, center in enumerate(cluster_centers_original):
        weighted_strength = 0
        profile = {}
        
        for j, feature in enumerate(feature_columns):
            feature_value = center[j]
            importance = feature_importance[feature]
            weighted_strength += feature_value * importance
            profile[feature] = round(feature_value, 3)
        
        cluster_strengths.append(weighted_strength)
        cluster_profiles[i] = profile

    sorted_cluster_ids = np.argsort(cluster_strengths)[::-1]

    tier_labels = ["Legendary", "Exceptional", "Advanced", "Skilled", "Intermediate", "Below Average", "Beginner"]
    cluster_id_to_tier = {}
    tier_profiles = {}

    for idx, cluster_id in enumerate(sorted_cluster_ids):
        if idx < len(tier_labels):
            tier = tier_labels[idx]
            cluster_id_to_tier[cluster_id] = tier
            tier_profiles[tier] = cluster_profiles[cluster_id]
        else:
            cluster_id_to_tier[cluster_id] = "Beginner"

    best_cluster_id = sorted_cluster_ids[0]
    best_cluster_center = cluster_centers_original[best_cluster_id]

    results = []
    for i, team in enumerate(team_features):
        cluster_id = labels[i]
        tier = cluster_id_to_tier[cluster_id]

        team_vector = np.array(
            [team["Elo_Rating"], team["Win_Rate"], team["Total_Matches"]]
        )

        distance_from_best = calculate_distance_from_best_cluster(
            team_vector, best_cluster_center
        )

        placement_explanation = generate_placement_explanation(
            team, tier_profiles[tier], feature_importance, team_vector, 
            cluster_centers_original[cluster_id], tier
        )

        results.append(
            {
                "Team_Name": team["Team_Name"],
                "Tier": tier,
                "Distance_From_Best": distance_from_best,
                "Cluster_ID": int(cluster_id),
                "Features": {
                    "Elo_Rating": team["Elo_Rating"],
                    "Win_Rate": round(
                        team["Win_Rate"], 2
                    ),
                    "Total_Matches": team["Total_Matches"],
                },
                "Tier_Profile": tier_profiles[tier],
                "Feature_Importance": feature_importance,
                "Placement_Explanation": placement_explanation,
            }
        )
    # Calculate distance from own cluster center for within-tier ranking
    for cluster_id in np.unique(labels):
        cluster_teams = [team for team in results if team["Cluster_ID"] == cluster_id]
        cluster_center = cluster_centers_original[cluster_id]

        for team in cluster_teams:
            features = np.array(
                [
                    team["Features"]["Elo_Rating"],
                    team["Features"]["Win_Rate"],
                    team["Features"]["Total_Matches"],
                ]
            )

            distance = np.linalg.norm(features - cluster_center)
            team["Cluster_Distance"] = round(distance, 2)

    tier_order = {tier: i for i, tier in enumerate(["Legendary", "Exceptional", "Advanced", "Skilled", "Intermediate", "Below Average", "Beginner"])}
    results.sort(key=lambda x: (tier_order[x["Tier"]], x["Distance_From_Best"], x["Cluster_Distance"]))

    current_tier = None
    rank_within_tier = 0

    for team in results:
        if team["Tier"] != current_tier:
            current_tier = team["Tier"]
            rank_within_tier = 1
        else:
            rank_within_tier += 1

        team["Rank_Within_Tier"] = rank_within_tier

    return results