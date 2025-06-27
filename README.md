# 🧠 Player Performance Scoring App (ML Pipeline with Azure Deployment)

A complete end-to-end machine learning pipeline that predicts and ranks **Total War: Rome 2** tournament players based on their performance metrics. Built with **Streamlit**, trained with **scikit-learn**, and deployed on **Azure App Service**.

I built this project in order to start getting into ML/Building ML pipelines in azure. This is why the project is rather simplistic, but I think it's a great way to get into the field.
---

## 📌 Overview

This project showcases a full ML lifecycle:

- 📊 **Data ingestion** from structured JSON
- 🛠️ **Feature engineering** including tier-based scoring
- 🧪 **Tier assignment** using unsupervised learning (K-Means clustering)
- 🌲 **Model training** using Random Forest regression
- ✅ **Evaluation** via Mean Squared Error (MSE)
- 🎯 **Prediction** of player scores
- 🌐 **Deployment** on Azure
- 📈 **Interactive dashboard** displaying the data via Streamlit

---

## 🔁 Pipeline Architecture


graph TD
A[Raw Player Data (JSON)] --> B[Preprocessing & Feature Engineering]

B --> C[Unsupervised K-Means Clustering]
C --> D[Cluster to Tier Mapping]
D --> E[Convert Tiers to Scores]

E --> F[Feature Matrix + Scores] --> G[Train Random Forest Regressor]
G --> H[Model Evaluation]
G --> I[Score Predictions]

I --> J[Streamlit Frontend]

---

## ⚙️ Features

- Clusters players into performance tiers using K-Means on core stats
- Maps each cluster to a tier label (e.g., Praetorian, Legionary) based on Win%
- Converts tiers into numerical scores as part of a hybrid scoring system
- Trains a machine learning model to predict custom performance scores
- Visualizes results through an interactive web interface
- Deploys the entire pipeline to the cloud with Azure App Service

---

## 🎯 Tier Assignment Model

Players are grouped into 4 tiers using K-Means clustering, an unsupervised learning algorithm applied to standardized performance features like Win %, K/D ratio, and playoff appearances.

The resulting clusters are then ranked by average Win % and mapped to named tiers:

**Cluster → Tier Mapping (example):**
- Cluster with highest Win % → Praetorian
- Next → Legionary
- Next → Hastati
- Lowest → Pleb

Each tier is then converted to an initial numeric score used as input to the supervised regression model.

---

## 📊 Model Performance

- **ML Model:** RandomForestRegressor
- **Test Set MSE:** 3292.92
- **Dataset:** 75 players × 5–8 performance stats

**Score distribution:**
- Mean: 808
- Min: 26
- Max: 1730
- Std Dev: ~480

---

## 🚀 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/player-ml-app.git
cd player-ml-app

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

```
PS: In order to showcase the progression of this mini project, I have separate json files for every step of the way:

Step 1 => Preprocess the raw json data and save it in a new json file 

Step 2 => Generate a second json file with players put into tiers via unsupervised learning 

Step 3 => Generate a third json file with final result => use supervised learning to predict the player's score
```