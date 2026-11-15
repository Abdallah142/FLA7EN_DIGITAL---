# FLA7EN_DIGITAL

# 🌱 NASA POWER · AI Crop Rotation & Stress Advisor

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random%20Forest-F7931E.svg)](https://scikit-learn.org/)
[![NASA POWER API](https://img.shields.io/badge/Data-NASA%20POWER%20API-0B3D91.svg)](https://power.larc.nasa.gov/)

An AI-powered precision agriculture platform that integrates real-time satellite climate telemetry from **NASA POWER API** with Machine Learning (**Random Forest Classifier**) to provide **24-hour early crop stress warnings** and **data-driven crop rotation strategies**.

---

## 🎯 Project Overview

Farmers and agronomists face increasing unpredictability due to heatwaves, shifting climate patterns, and soil moisture depletion. This platform bridges the gap between raw satellite observations and actionable field decisions without requiring expensive ground IoT sensors:

1. **AI Early Warning System (Next-Day Stress Forecast):** Uses daily satellite telemetry (`T2M`, `PRECTOTCORR`, `GWETTOP`, `EVPTRNS`) with time-series shifting to predict thermal and drought stress 24 hours in advance with **95.89% validation accuracy**.
2. **Smart Crop Rotation Advisor:** Analyzes 3-year historical monthly climate patterns, soil types (Clay, Sandy, Loamy), and farmer priorities (water conservation, soil health, or income diversification) to recommend resilient multi-season crop sequences.

---

## ✨ Key Features

* **🛰️ Live NASA POWER Integration:** Automated ETL pipeline fetching daily and monthly agro-climatology data for any GPS coordinates globally, including quick presets (*Nile Delta*, *Central Valley*, *Punjab*).
* **🤖 Predictive Machine Learning:** `RandomForestClassifier` trained on 1,096+ daily satellite records with `StandardScaler` normalization and `joblib` persistence for instant inference.
* **📊 Data Science & Model Diagnostics:** Comprehensive statistical analysis including correlation matrices, cross-validation, and feature importance ranking.
* **🌐 Bilingual Interactive Dashboard:** Built with **Streamlit** and **Plotly Express**, offering seamless **English & Arabic (RTL)** switching, interactive water-balance charts, seasonal trends, and one-click CSV data export.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Machine Learning & Data Analysis:** `scikit-learn`, `pandas`, `numpy`, `joblib`
* **Frontend & Visualization:** `Streamlit`, `Plotly Express`
* **API & Telemetry:** NASA POWER Daily & Monthly Point APIs

---

## 📂 Project Structure

```text
├── data_read.py              # NASA POWER ETL pipeline & Random Forest model training
├── ui_scrept.py              # Main Streamlit bilingual dashboard & AI inference app
├── graph.py                  # Matplotlib data science & model performance plotting script
├── crop_stress_model.pkl     # Pre-trained Random Forest model artifact
├── crop_scaler.pkl           # Fitted StandardScaler artifact
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the AI Model (Generates `.pkl` files)
```bash
python data_read.py
```

### 4. Run Model Performance Visualizations
```bash
python graph.py
```

### 5. Launch the Dashboard
```bash
streamlit run ui_scrept.py
```

---

## ⚠️ Disclaimer
This platform is built for agricultural decision support and climate screening. Always validate irrigation adjustments and planting schedules with local agronomists and field soil tests.
