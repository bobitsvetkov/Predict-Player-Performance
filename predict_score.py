import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from utils import format_decimal_to_percent_columns
from tier_assignment import assign_tiers


def predict_battle_performance(
    input_file="player_stats_cleaned.json", output_file="player_data.json"
):
    df = pd.read_json(input_file)
    df.fillna(0, inplace=True)
    skill = df["K/D ratio"] * df["Chevrons/game"]
    skill_norm = skill / skill.max()
    win_norm = df["Win %"] / df["Win %"].max()
    playoff_rate = df["Playoff Rate"] / df["Playoff Rate"].max()
    penalty = ((skill_norm - win_norm - playoff_rate).clip(lower=0) ** 2) * 1.5

    df["Battle_Performance"] = (
        5 * skill_norm + 10 * win_norm + 5 * playoff_rate - 10 * penalty
    )

    # Normalize Battle_Performance to a 0-100 scale based on min and max scores
    min_score = df["Battle_Performance"].min()
    max_score = df["Battle_Performance"].max()

    df["Battle_Performance"] = (
        (df["Battle_Performance"] - min_score) / (max_score - min_score)
    ) * 100

    # ensure no negative or >100 scores after normalization
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

    X = df[features]
    y = df["Battle_Performance"]

    print(f"Dataset size: {len(df)} players")
    print("Battle_Performance distribution:")
    print(y.describe())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=42, test_size=0.2
    )

    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
    }

    rf = RandomForestRegressor(random_state=42)

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        n_jobs=-1,
        verbose=1,
    )

    grid_search.fit(X_train, y_train)

    print("Best hyperparameters found:")
    print(grid_search.best_params_)

    best_model = grid_search.best_estimator_

    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error on test set: {mse:.2f}")
    print(f"R² on test set: {r2:.3f}")

    df.loc[X_test.index, "Predicted_Score_Validation"] = y_pred

    df["Predicted_Score"] = best_model.predict(X)
    df["Predicted_Score"] = df["Predicted_Score"].round(2)
    df = assign_tiers(df, score_col="Predicted_Score")
    df = format_decimal_to_percent_columns(df)
    df_sorted = df.sort_values(by="Predicted_Score", ascending=False)
    df_sorted.to_json(output_file, orient="records", indent=4)

    print(df["Tier"].value_counts())

    return df_sorted


if __name__ == "__main__":
    df_result = predict_battle_performance()
    print("Model training, prediction and tier assignment complete.")
