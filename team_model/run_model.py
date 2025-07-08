import os
from typing import List, Dict, Any, Optional
from utils import load_team_data, extract_team_features
from clustering import prepare_data_for_clustering, perform_clustering
from tier_assignment import assign_tiers_and_rank_teams
from tier_analyzer import (
    analyze_tier_placement,
    find_potential_outliers,
)
from save_tier_results import save_tier_results, print_tier_summary


def create_tier_classification_pipeline(
    team_data_path: str, output_dir: str
) -> Optional[List[Dict[str, Any]]]:
    """Main pipeline for tier classification"""
    try:
        os.makedirs(output_dir, exist_ok=True)

        print("Loading team data...")
        teams_data = load_team_data(team_data_path)
        print(f"Loaded {len(teams_data)} teams")

        team_features = [extract_team_features(team) for team in teams_data]
        print(f"Extracted features for {len(team_features)} teams")

        print("Preparing data for clustering...")
        X_scaled, scaler, feature_columns = prepare_data_for_clustering(team_features)
        print(f"Prepared data with shape: {X_scaled.shape}")

        print("Performing clustering...")
        labels, cluster_centers_scaled = perform_clustering(X_scaled, n_clusters=7)
        print(f"Clustering complete with {len(set(labels))} clusters")

        print("Assigning tiers and ranking teams...")
        tiered_teams = assign_tiers_and_rank_teams(
            team_features,
            X_scaled,
            labels,
            cluster_centers_scaled,
            scaler,
            feature_columns,
        )

        if tiered_teams is None:
            print("Error: tiered_teams is None!")
            return None

        print(f"Tier assignment complete for {len(tiered_teams)} teams")

        print("Analyzing tier placements...")
        tiered_teams = analyze_tier_placement(tiered_teams)

        # print("Refining team tiers based on confidence...")
        # tiered_teams = refine_team_tiers(tiered_teams)

        print("Identifying potential outliers...")
        outliers = find_potential_outliers(tiered_teams)
        if outliers:
            print(f"Top potential outliers in tier assignments: {', '.join(outliers)}")
        else:
            print("No significant outliers found.")
        print("Saving results...")
        output_file = os.path.join(output_dir, "team_tiers.json")
        save_tier_results(tiered_teams, output_file)

        return tiered_teams

    except Exception as e:
        print(f"Error in pipeline: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def run_model():
    """Main entry point"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    team_data_file = os.path.normpath(
        os.path.join(current_dir, "..", "data", "elo_rating.json")
    )

    results = create_tier_classification_pipeline(
        team_data_path=team_data_file, output_dir="data"
    )

    if results:
        print_tier_summary(results)

        print(f"\nClustering results saved to 'data/team_tiers.json'")
    else:
        print("Clustering pipeline failed to generate results")


if __name__ == "__main__":
    run_model()
