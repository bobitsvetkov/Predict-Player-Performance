import numpy as np
from typing import List, Dict, Any


def analyze_tier_placement(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze team placements and add explanations for potentially misplaced teams"""

    if not results:
        return results

    # Calculate statistics for each tier
    tier_stats = {}
    for team in results:
        tier = team["Tier"]
        if tier not in tier_stats:
            tier_stats[tier] = {"distances": [], "teams": []}
        tier_stats[tier]["distances"].append(team["Distance_From_Best"])
        tier_stats[tier]["teams"].append(team)

    # Calculate thresholds for each tier
    tier_thresholds = {}
    for tier, stats in tier_stats.items():
        distances = stats["distances"]
        if len(distances) > 1:
            avg_distance = np.mean(distances)
            std_distance = np.std(distances)
            tier_thresholds[tier] = {
                "avg": avg_distance,
                "upper_bound": avg_distance
                + (1.5 * std_distance),  # Teams much worse than tier average
                "lower_bound": avg_distance
                - (1.5 * std_distance),  # Teams much better than tier average
            }
        else:
            tier_thresholds[tier] = {
                "avg": distances[0],
                "upper_bound": distances[0],
                "lower_bound": distances[0],
            }

    # Add explanations to results
    tier_order = ["S", "A", "B", "C", "D", "E", "F"]

    for team in results:
        tier = team["Tier"]
        distance = team["Distance_From_Best"]
        explanation = ""

        try:
            current_tier_idx = tier_order.index(tier)
        except ValueError:
            # Handle case where tier is not in expected order
            explanation = f"Standard {tier}-tier performance."
            team["Placement_Analysis"] = explanation
            continue

        # Check if team is much better than their tier average
        if distance < tier_thresholds[tier]["lower_bound"]:
            if current_tier_idx > 0:  # Not already in S-tier
                better_tier = tier_order[current_tier_idx - 1]
                explanation = f"Performs significantly better than typical {tier}-tier teams. Could potentially be {better_tier}-tier."
            else:
                explanation = f"Elite performer within {tier}-tier."

        # Check if team is much worse than their tier average
        elif distance > tier_thresholds[tier]["upper_bound"]:
            if current_tier_idx < len(tier_order) - 1:  # Not already in F-tier
                worse_tier = tier_order[current_tier_idx + 1]
                explanation = f"Performs significantly worse than typical {tier}-tier teams. Might be closer to {worse_tier}-tier level."
            else:
                explanation = f"Below average for {tier}-tier."

        # Standard placement
        else:
            if distance <= tier_thresholds[tier]["avg"]:
                explanation = f"Solid {tier}-tier performance, above tier average."
            else:
                explanation = f"Typical {tier}-tier performance, below tier average."

        team["Placement_Analysis"] = explanation

    return results


def find_potential_outliers(results: List[Dict[str, Any]]) -> List[str]:
    """Find teams that might be outliers in their tier"""
    outliers = []

    # Group by tier
    tiers = {}
    for team in results:
        tier = team["Tier"]
        if tier not in tiers:
            tiers[tier] = []
        tiers[tier].append(team)

    # Find outliers in each tier
    for tier, teams in tiers.items():
        if len(teams) < 3:  # Skip tiers with too few teams
            continue

        # Calculate tier statistics
        elos = [t["Features"]["Elo_Rating"] for t in teams]
        win_rates = [t["Features"]["Win_Rate"] for t in teams]

        elo_mean, elo_std = np.mean(elos), np.std(elos)
        wr_mean, wr_std = np.mean(win_rates), np.std(win_rates)

        # Find teams that are more than 1.5 standard deviations away
        for team in teams:
            elo_z = abs(team["Features"]["Elo_Rating"] - elo_mean) / (elo_std + 1e-6)
            wr_z = abs(team["Features"]["Win_Rate"] - wr_mean) / (wr_std + 1e-6)

            if elo_z > 1.5 or wr_z > 1.5:
                outliers.append(team["Team_Name"])

    return outliers[:10]  # Return top 10 outliers