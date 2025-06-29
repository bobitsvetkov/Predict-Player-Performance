import pandas as pd
import numpy as np


def format_decimal_to_percent_columns(df):
    percent_fields = ["Win %", "Playoff Rate"]
    for col in percent_fields:
        df[col] = df[col].apply(lambda x: f"{x * 100:.1f}%" if pd.notnull(x) else x)
    return df


def calculate_custom_score(df):
    return (
        (df["Win %"] * 400)
        + (df["Playoff Appearances"] * 25)
        + (df["Chevrons/game"] * 30)
        + (df["K/D ratio"] * 100)
    )


def compute_percentiles(df, features):
    percentiles = {}
    for feature in features:
        percentiles[feature] = df[feature].rank(pct=True, ascending=True)
    return percentiles


def percent_str_to_float(s):
    if isinstance(s, str) and s.endswith("%"):
        return float(s.strip("%")) / 100
    elif pd.isnull(s):
        return np.nan
    else:
        return float(s)