import json
from typing import List, Dict, Any


def load_team_data(file_path: str) -> List[Dict[str, Any]]:
    """Load team data from JSON file"""
    with open(file_path, "r") as file:
        data = json.load(file)
    return data["teams"]


def calculate_win_rate(matches: List[Dict[str, Any]]) -> float:
    """Calculate win rate from matches"""
    if not matches:
        return 0.0

    wins = sum(1 for match in matches if match["Result"] == "Win")
    total_matches = len(matches)
    return wins / total_matches if total_matches > 0 else 0.0


def extract_team_features(team_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract features from team data"""
    elo_rating = round(team_data["Elo Rating"], 2)

    # Calculate win rate from matches
    matches = team_data.get("Matches", [])
    win_rate = calculate_win_rate(matches)

    return {
        "Team_Name": team_data["Team Name"],
        "Elo_Rating": elo_rating,
        "Win_Rate": round(win_rate * 100, 2),  # Convert to percentage (0-100) for training
        "Total_Matches": len(matches),
    }