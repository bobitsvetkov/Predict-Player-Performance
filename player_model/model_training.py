from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def train_and_evaluate_model(X, y):
    """
    Trains a RandomForestRegressor model using GridSearchCV and evaluates its performance.

    Args:
        X (pd.DataFrame): Features for training and testing.
        y (pd.Series): Target variable for training and testing.

    Returns:
        tuple: A tuple containing:
            - best_model (RandomForestRegressor): The best trained model.
            - X_test_index (pd.Index): Index of the test set from the original DataFrame.
            - y_pred_test (np.array): Predictions on the test set.
            - mse (float): Mean Squared Error on the test set.
            - r2 (float): R-squared score on the test set.
    """
    print(f"Dataset size: {len(X)} players")
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
    y_pred_test = best_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred_test)
    r2 = r2_score(y_test, y_pred_test)

    print(f"Mean Squared Error on test set: {mse:.2f}")
    print(f"R² on test set: {r2:.3f}")

    return best_model, X_test.index, y_pred_test, mse, r2