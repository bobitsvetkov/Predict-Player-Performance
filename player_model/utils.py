import pandas as pd
import shap


def explain_model_with_shap(model, X):
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)
    return shap_values


def format_decimal_to_percent_columns(df):
    percent_fields = ["Win %", "Playoff Rate"]
    for col in percent_fields:
        df[col] = df[col].apply(lambda x: f"{x * 100:.1f}%" if pd.notnull(x) else x)
    return df