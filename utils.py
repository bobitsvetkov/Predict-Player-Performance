def format_decimal_to_percent(win_decimal):
    win_percent_str = f"{win_decimal * 100:.1f}%"
    return win_percent_str


def calculate_custom_score(df):
    return (
        (df["Win %"] * 400)
        + (df["Games Played"] * 2)
        + (df["Championships"] * 50)
        + (df["Playoff Appearances"] * 25)
        + df["Initial_Score"]
    )
