import numpy as np

def assign_tiers(df, score_col="Predicted_Score"):
    tier_names = [
        "Champion",
        "Good Player",
        "Above Average",
        "Average",
        "Below Average",
        "New Player",
    ]

    percentiles = [90, 70, 50, 30, 10, 0]

    thresholds = np.percentile(df[score_col], percentiles)

    def tier_func(score):
        for i, threshold in enumerate(thresholds):
            if score >= threshold:
                return tier_names[i]
        return tier_names[-1]

    df["Tier"] = df[score_col].apply(tier_func)
    return df
