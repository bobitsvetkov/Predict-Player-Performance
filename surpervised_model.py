import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from utils import calculate_custom_score

tier_score_map = {
    "Pleb": 0,
    "Hastati": 500,
    "Legionary": 750,
    "Praetorian": 1000,
}

def train_score_model(input_file="player_tiers.json", output_file="player_data.json"):
    df = pd.read_json(input_file)
    df.fillna(0, inplace=True)

    df["Initial_Score"] = df["Tier"].map(tier_score_map).fillna(0)

    df["Custom_Score"] = calculate_custom_score(df)

    features = [
        "Championships",
        "Playoff Rate",
        "Chevrons/game",
        "K/D ratio",
        "Playoff Appearances",
        "Runner-ups",
        "Third Places",
        "Games Played",
        "Initial_Score",
    ]

    X = df[features]
    y = df["Custom_Score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=42, test_size=0.2
    )

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error on test set: {mse:.2f}")

    df.loc[X_test.index, "Predicted_Score_Validation"] = y_pred

    df["Predicted_Score"] = model.predict(X)

    df_sorted = df.sort_values(by="Predicted_Score", ascending=False)

    df_sorted.to_json(output_file, orient="records", indent=4)
    print(f"Saved final player scores with predictions to {output_file}")
    print(df["Custom_Score"].describe())


if __name__ == "__main__":
    train_score_model()
    print("Model training complete and data saved.")
