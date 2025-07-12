import pandas as pd
import os


def load_data(input_file):
    """
    Loads player data from a JSON file.

    Args:
        input_file (str): Absolute path to the JSON file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    df = pd.read_json(input_file)
    return df


def preprocess_data(input_file):
    """
    Loads player data, handles missing values, and calculates initial
    battle performance metrics and interaction features.

    Args:
        input_file (str): Path to the input JSON file.

    Returns:
        pd.DataFrame: Processed DataFrame with Battle_Performance and
                      interaction features.
        list: Feature column names.
    """
    df = load_data(input_file)
    df.fillna(0, inplace=True)

    skill = df["K/D ratio"] * df["Chevrons/game"]
    skill_norm = skill / skill.max()

    win_norm = df["Win %"] / df["Win %"].max()
    playoff_rate = df["Playoff Rate"] / df["Playoff Rate"].max()

    penalty = ((skill_norm - win_norm - playoff_rate).clip(lower=0) ** 2) * 1.5

    df["Battle_Performance"] = (
        5 * skill_norm + 10 * win_norm + 5 * playoff_rate - 10 * penalty
    )

    min_score = df["Battle_Performance"].min()
    max_score = df["Battle_Performance"].max()
    df["Battle_Performance"] = (
        (df["Battle_Performance"] - min_score) / (max_score - min_score)
    ) * 100
    df["Battle_Performance"] = df["Battle_Performance"].clip(lower=0, upper=100)

    df["Win_Playoff_Interaction"] = (df["Win %"] * 100) * (df["Playoff Rate"] * 100)
    df["Playoff_Championship_Interaction"] = (
        df["Playoff Appearances"] * df["Championships"]
    )

    features = [
        "Chevrons/game",
        "Win %",
        "Playoff Rate",
        "K/D ratio",
        "Championships",
        "Playoff Appearances",
        "Win_Playoff_Interaction",
        "Playoff_Championship_Interaction",
    ]

    return df, features
