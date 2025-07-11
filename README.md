# 🧠 Player Performance Scoring App (ML Pipeline with Streamlit Cloud Deployment)

A complete end-to-end machine learning pipeline that predicts and ranks **Total War: Rome 2** tournament players based on their performance metrics. Built with **Streamlit**, trained with **scikit-learn**, and deployed on **Streamlit Cloud**. Might change if it gets more traffic.

## Project Learning Points

I built this project in order to start getting into ML/Building ML pipelines. I learned various things while doing it. The most important thing was how to make sure that my data is ready to be trained on and well how to do data preprocessing. This is why the project is rather simplistic, but I think it's a great way to get into the field. Just as an example in my data there were many plays with strange stats, such as 0 kd/0 total kills but 60% win rate, or 20 total games but 16 wins and 10 losses.

---

## 📌 Overview

This project demonstrates a complete machine learning pipeline for evaluating and ranking tournament players based on performance metrics. It integrates data engineering, percentile-based tiering, regression modeling, real tiering based on clustering and interactive visualization.

- 📥 **Data Ingestion** from structured JSON inputs  
- 🧱 **Feature Engineering** including win rate, ELO rating, and match volume  
- 🏷️ **Tier Assignment** using two complementary approaches:  
  - Manual Tiering: Based on percentiles of predicted player scores (supervised regression)  
  - Unsupervised Tiering: Based on K-Means clustering of team performance metrics, assigning each team to a cluster  
- 🌲 **Supervised Learning** using Random Forest Regressor to predict player scores  
- 📊 **Model Evaluation** using Mean Squared Error (MSE) and R²  
- 🎯 **Score Prediction** and tier-based ranking  
- 🌐 **Deployment** on Streamlit Cloud (will change later if project gains enough traction)  
- 📈 **Interactive Streamlit Dashboard** for player insights and rankings  

---

## 🔁 Pipeline Architecture

1. 🔄 **Data Preprocessing** & Feature Engineering  
2. 🏷️ **Tier Assignment** using clustering for teams and manual for players
3. 🧪 **Train/Test Split** & Feature Matrix Construction  
4. 🌲 **Random Forest Regression** (optimized with Grid Search)
    - 📉 Model Evaluation using **MSE** and **R²**
    - 🎯 **Score Prediction** for All Players (using formula to help out the model due to lack of enough data)
5. 📊 **Streamlit Dashboard** for displaying training result

---

## 📊 Supervised Model Performance

- **ML Model:** RandomForestRegressor (tuned with GridSearchCV, 5-fold cross-validation)
- **Test Set MSE:** 13.21
- **Dataset:** 75 players × 5–8 performance stats
- **R²:**  0.965 (using manual formula due to lack of enough data)

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
