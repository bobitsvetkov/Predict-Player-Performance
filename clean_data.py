import json
with open("player_stats_historical.json", "r") as f:
    raw_data = json.load(f)

cleaned_data = []
for record in raw_data:
    cleaned_record = {}

    for key, value in record.items():
        if value == "":
            cleaned_record[key] = None
            continue
        if isinstance(value, str) and "," in value:
            value = value.replace(",", "")
        if isinstance(value, str) and value.endswith("%"):
            try:
                cleaned_record[key] = float(value.strip("%")) / 100
            except ValueError:
                cleaned_record[key] = None
            continue
        try:
            cleaned_record[key] = float(value)
        except (ValueError, TypeError):
            cleaned_record[key] = value

    cleaned_data.append(cleaned_record)

filtered_data = [
    player for player in cleaned_data if (player.get("Games Played", 0) or 0) >= 12
]

with open("player_stats_cleaned.json", "w") as f:
    json.dump(filtered_data, f, indent=4)

print("Cleaned data saved to player_stats_cleaned.json")
