import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_json("player_stats_cleaned.json")
df.fillna(0, inplace=True)

features = [
    "Championships",
    "Playoff Rate",
    "Win %",
    "Chevrons/game",
    "K/D ratio",
    "Playoff Appearances",
    "Runner-ups",
    "Third Places",
]


df_clean = df.dropna(subset=features).copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean[features])

kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

df_clean["Cluster"] = clusters

cluster_summary = df_clean.groupby("Cluster")["Win %"].mean().sort_values(ascending=False)

tier_map = {cluster: tier for cluster, tier in zip(cluster_summary.index, ["Praetorian", "Legionary", "Hastati", "Pleb"])}

df_clean["Tier"] = df_clean["Cluster"].map(tier_map)

df_clean.to_json("player_tiers.json", orient="records", indent=4)