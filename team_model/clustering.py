import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def prepare_data_for_clustering(
    team_features: List[Dict[str, Any]],
) -> Tuple[np.ndarray, StandardScaler, List[str]]:
    """Prepare data for clustering"""
    feature_columns = ["Elo_Rating", "Win_Rate", "Total_Matches"]

    X = np.array(
        [[team[feature] for feature in feature_columns] for team in team_features]
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler, feature_columns


def perform_clustering(
    X_scaled: np.ndarray, n_clusters: int = 7, random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """Perform K-means clustering"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans.fit_predict(X_scaled)
    return (
        labels,
        kmeans.cluster_centers_,
    )


def calculate_feature_importance(
    cluster_centers: np.ndarray, feature_columns: List[str]
) -> Dict[str, float]:
    """Calculate feature importance based on cluster center variance"""
    feature_importance = {}

    # Calculate variance for each feature across clusters
    for i, feature in enumerate(feature_columns):
        feature_values = cluster_centers[:, i]
        variance = np.var(feature_values)
        feature_importance[feature] = variance

    # Normalize importance scores to sum to 1
    total_importance = sum(feature_importance.values())
    if total_importance > 0:
        for feature in feature_importance:
            feature_importance[feature] /= total_importance

    return feature_importance


def calculate_distance_from_best_cluster(
    team_features: np.ndarray, best_cluster_center: np.ndarray
) -> float:
    """Calculate how close a team is to the best performing cluster center"""
    distance = np.linalg.norm(team_features - best_cluster_center)
    return round(distance, 2)
