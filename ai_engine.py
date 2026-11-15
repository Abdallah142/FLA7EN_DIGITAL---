import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class UnifiedFarmAI:
    def __init__(self, file_path=None, lat=None, lon=None):
        self.file_path = file_path
        self.lat = lat
        self.lon = lon
        self.df = None

    def load_and_clean_data(self):
        if self.file_path and os.path.exists(self.file_path):
            ext = os.path.splitext(self.file_path)[1].lower()
            if ext == '.csv':
                self.df = pd.read_csv(self.file_path)
            elif ext in ['.xls', '.xlsx']:
                self.df = pd.read_excel(self.file_path)
            elif ext == '.json':
                self.df = pd.read_json(self.file_path)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        elif self.lat and self.lon:
            url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
            params = {
                "parameters": "T2M,PRECTOTCORR,GWETTOP,EVPTRNS",
                "community": "AG",
                "longitude": self.lon,
                "latitude": self.lat,
                "start": 2022,
                "end": 2025,
                "format": "JSON"
            }
            response = requests.get(url, params=params, timeout=15)
            data = response.json()
            properties = data['properties']['parameter']
            records = []
            for date_key in properties['T2M'].keys():
                if not date_key.endswith("13"):
                    records.append({
                        "Temp_C": properties['T2M'][date_key],
                        "Rain_mm": properties['PRECTOTCORR'][date_key],
                        "Soil_Moisture": properties['GWETTOP'][date_key],
                        "Evap_mm": properties['EVPTRNS'][date_key]
                    })
            self.df = pd.DataFrame(records)

        if self.df is not None and not self.df.empty:
            df = self.df.copy()
            df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
            df = df.drop_duplicates()
            df = df.dropna(how='all')
            
            for col in df.select_dtypes(include=['float64', 'int64']).columns:
                df[col] = df[col].fillna(df[col].mean())
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].fillna("Unknown")
                
            self.df = df
            return df
        return None

    def run_ai_model(self):
        if self.df is None or self.df.empty:
            return None

        expected_features = ['temp_c', 'rain_mm', 'soil_moisture', 'evap_mm']
        for feat in expected_features:
            if feat not in self.df.columns:
                return f"Missing required column in dataset: {feat}"

        X = self.df[expected_features]
        y = np.where((X['temp_c'] > 26) & (X['soil_moisture'] < 0.4), 1, 0)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X_scaled, y)

        latest_data = X_scaled[-1:].reshape(1, -1)
        prediction = model.predict(latest_data)[0]
        probability = model.predict_proba(latest_data)[0][1]

        return {
            "stress_predicted": bool(prediction),
            "stress_probability": float(probability),
            "avg_temp": float(self.df['temp_c'].mean()),
            "avg_moisture": float(self.df['soil_moisture'].mean()),
            "total_rows": len(self.df)
        }

st.set_page_config(page_title="NASA Unified Farm AI", layout="wide")
st.title("🌱 NASA & Custom Dataset Integrated Farm AI")

data_source = st.sidebar.radio("Choose Data Source:", ["Upload Competition Dataset", "Fetch Live NASA API"])

file_path_input = None
lat, lon = None, None

if data_source == "Upload Competition Dataset":
    uploaded_file = st.sidebar.file_uploader("Upload CSV, Excel, or JSON file", type=["csv", "xlsx", "json"])
    if uploaded_file is not None:
        file_path_input = "temp_uploaded_data.csv"
        with open(file_path_input, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success("File uploaded successfully!")
else:
    lat = st.sidebar.number_input("Latitude", value=30.0444, format="%.4f")
    lon = st.sidebar.number_input("Longitude", value=31.2357, format="%.4f")

if st.sidebar.button("Run Complete Pipeline"):
    with st.spinner("Loading data, cleaning it, and running Random Forest AI model..."):
        system = UnifiedFarmAI(file_path=file_path_input, lat=lat, lon=lon)
        clean_df = system.load_and_clean_data()
        
        if clean_df is not None:
            st.success("Data Loader & Cleaner executed successfully!")
            results = system.run_ai_model()
            
            if isinstance(results, dict):
                col1, col2, col3 = st.columns(3)
                col1.metric("Average Temperature", f"{results['avg_temp']:.1f} °C")
                col2.metric("Soil Moisture", f"{results['avg_moisture']:.2f}")
                col3.metric("Stress Probability", f"{results['stress_probability']*100:.1f}%")
                
                st.subheader("Cleaned Dataset Preview")
                st.dataframe(clean_df.head(5))
            else:
                st.error(results)
        else:
            st.error("Failed to load or process data.")