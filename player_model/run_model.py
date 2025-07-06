import shap
import json
from data_preprocessing import preprocess_data
from model_training import train_and_evaluate_model
from prediction import predict_and_assign_tiers
from utils.utils import format_decimal_to_percent_columns, explain_model_with_shap


def run_model(
    input_file="data/player_stats_cleaned.json", output_file="data/player_data.json"
):
    """
    Orchestrates the entire process of predicting battle performance,
    training a model, assigning tiers, and saving results.
    """
    print("Starting battle performance prediction process...")

    df, features = preprocess_data(input_file)

    X = df[features]
    y = df["Battle_Performance"]

    best_model, X_test_index, y_pred_test, mse, r2 = train_and_evaluate_model(X, y)

    model_summary = {
        "model_type": "RandomForestRegressor",
        "best_hyperparameters": best_model.get_params(),
        "test_mse": round(mse, 2),
        "test_r2": round(r2, 3),
        "training_data_size": len(X),
        "test_data_size": len(X_test_index),
    }

    with open(output_file, "w") as f:
        json.dump(model_summary, f, indent=4)
    print(f"\nModel summary saved to {output_file}")

    if r2 < 0.70:
        print("WARNING: Model performance (R² < 0.70) is below acceptable levels.")
        print("Consider improving the model or investigating the data.")

    shap_values = explain_model_with_shap(best_model, X)

    shap.summary_plot(shap_values, X)

    # 3. Predict and Assign Tiers
    df = predict_and_assign_tiers(df, best_model, features, X_test_index, y_pred_test)

    # 4. Save Results
    df = format_decimal_to_percent_columns(df)
    df_sorted = df.sort_values(by="Predicted_Score", ascending=False)
    df_sorted.to_json(output_file, orient="records", indent=4)
    print("\nTier distribution in final output:")
    print(df["Tier"].value_counts())

    print("Model training, prediction and tier assignment complete.")
    return df_sorted


if __name__ == "__main__":
    df_final_results = run_model()
