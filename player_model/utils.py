import pandas as pd
import shap


def explain_model_with_shap(model, X):
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)
    return shap_values


def format_decimal_columns(df):
    decimal_fields = [
        "Win %",
        "Playoff Rate",
        "K/D ratio",
        "Chevrons/game",
        "Playoff Rate",
    ]
    for col in decimal_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round(2)
    return df