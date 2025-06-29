# 🧠 Player Performance Scoring App (ML Pipeline with Azure Deployment)

A complete end-to-end machine learning pipeline that predicts and ranks **Total War: Rome 2** tournament players based on their performance metrics. Built with **Streamlit**, trained with **scikit-learn**, and deployed on **Azure App Service**.

I built this project in order to start getting into ML/Building ML pipelines in azure. This is why the project is rather simplistic, but I think it's a great way to get into the field.
---

## 📌 Overview

This project demonstrates a complete machine learning pipeline for evaluating and ranking tournament players based on performance metrics. It integrates data engineering, percentile-based tiering, regression modeling, and interactive visualization.

- 📥 **Data Ingestion** from structured JSON inputs  
- 🧱 **Feature Engineering** with custom performance metrics  
- 🏷️ **Tier Assignment** based on percentiles of predicted scores  
- 🌲 **Supervised Learning** using Random Forest Regressor to predict player scores  
- 📊 **Model Evaluation** using Mean Squared Error (MSE) and R²  
- 🎯 **Score Prediction** and tier-based ranking  
- 🌐 **Deployment** on Azure App Service  
- 📈 **Interactive Streamlit Dashboard** for player insights and rankings

---

## 🔁 Pipeline Architecture

1. 🔄 **Data Preprocessing** & Feature Engineering  
2. 🏷️ **Tier Assignment** using score percentiles (no clustering)  
3. 🧮 **Battle Performance Score** Calculation  
4. 🧪 **Train/Test Split** & Feature Matrix Construction  
5. 🌲 **Random Forest Regression** (optimized with Grid Search)
    - 📉 Model Evaluation using **MSE** and **R²**
    - 🎯 **Score Prediction** for All Players  
6. 📊 **Streamlit Dashboard** for displaying training result

---

## ⚙️ Features

- Calculates a **custom Battle Performance Score** combining K/D ratio, chevrons, win rate, and playoff participation
- Trains a **Random Forest regression model** to predict scores based on key features  
- Assigns **performance tiers** (e.g., Champion, Good Player) using **score percentiles** 
- Implements a **hybrid scoring system** that blends skill and outcome-based metrics  
- Provides an **interactive web interface** for player comparison and score breakdown  

---

## 🎯 Tier Assignment Model

Players are assigned to performance tiers based on their **Battle Performance Score percentiles** rather than clustering.

The score is computed using a custom formula that weights skill (K/D ratio, chevrons per game) and outcomes (Win %, Playoff Rate), with penalties for bad performance.

Tiers are mapped from score percentiles:

**Percentile → Tier Mapping (example):**
- Top 10% → Champion
- Next 20% → Good Player
- Next 30% → Above Average
- Bottom 40% → Average

These tiers provide intuitive performance labels and are used in visualizations to help compare players more easily.

---

## 📊 Model Performance

- **ML Model:** RandomForestRegressor (tuned with GridSearchCV, 5-fold cross-validation)
- **Test Set MSE:** 13.21
- **Dataset:** 75 players × 5–8 performance stats
- **R²:**  0.965

**Score distribution:**
- Mean: 56.84
- Min: 0.00
- Max: 100.00
- Standard Deviation: 23.51

---

## 🚀 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/player-ml-app.git
cd Predict-Player-Performance

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

Step 2 => Train the model and save the data in a separate json file: player_data.json
```