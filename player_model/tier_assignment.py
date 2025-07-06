import pandas as pd
import numpy as np

def assign_tiers(df, score_col="Predicted_Score"):
    tier_names = ["S", "A", "B", "C", "D", "E", "F"]
    percentiles = [95, 85, 70, 50, 30, 10]

    if df.empty or df[score_col].isnull().all():
        df["Tier"] = "F"
        return df

    if len(df[score_col].dropna()) < len(percentiles):
        print(f"Warning: Not enough non-NaN scores ({len(df[score_col].dropna())}) to calculate all {len(percentiles)} percentiles. Assigning 'F' to all players.")
        df["Tier"] = "F"
        return df

    thresholds = np.percentile(df[score_col].dropna(), percentiles)

    def tier_func(score):
        if pd.isna(score):
            return "F"
        for i, threshold in enumerate(thresholds):
            if score >= threshold:
                return tier_names[i]
        return tier_names[-1]

    df["Tier"] = df[score_col].apply(tier_func)
    return df