from tier_assignment import assign_tiers

def predict_and_assign_tiers(df, best_model, features, X_test_index, y_pred_test):
    """
    Makes predictions on the full dataset and assigns tiers based on the predictions.

    Args:
        df (pd.DataFrame): The original DataFrame.
        best_model (RandomForestRegressor): The trained model.
        features (list): List of feature names used for prediction.
        X_test_index (pd.Index): Index of the test set from the original DataFrame.
        y_pred_test (np.array): Predicted values for the test set.

    Returns:
        pd.DataFrame: DataFrame with predicted scores and assigned tiers.
    """
    df.loc[X_test_index, "Predicted_Score_Validation"] = y_pred_test
    df["Predicted_Score"] = best_model.predict(df[features])
    df["Predicted_Score"] = df["Predicted_Score"].round(2)

    df = assign_tiers(df, score_col="Predicted_Score")
    return df