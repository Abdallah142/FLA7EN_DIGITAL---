import os
import joblib
import numpy as np
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class NASAAPIProcessor:

  def __init__(self, lat, lon, start_date, end_date):
    self.lat = lat
    self.lon = lon
    self.start_date = start_date
    self.end_date = end_date
    self.df = None
    self.model_path = "crop_stress_model.pkl"
    self.scaler_path = "crop_scaler.pkl"

  def fetch_data_from_nasa(self):
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "start": self.start_date,
        "end": self.end_date,
        "latitude": self.lat,
        "longitude": self.lon,
        "community": "ag",
        "parameters": "T2M,PRECTOTCORR,GWETTOP,EVPTRNS",
        "format": "JSON",
    }

    try:
      print("Sending request to NASA POWER Daily API...")
      response = requests.get(url, params=params, timeout=15)
      response.raise_for_status()
      data = response.json()

      properties = data["properties"]["parameter"]
      records = []
      dates = list(properties["T2M"].keys())

      for date_key in dates:
        records.append({
            "Date": date_key,
            "Temp_C": properties["T2M"][date_key],
            "Rain_mm": properties["PRECTOTCORR"][date_key],
            "Soil_Moisture": properties["GWETTOP"][date_key],
            "Evap_mm": properties["EVPTRNS"][date_key],
        })

      df = pd.DataFrame(records)

      # 1. فلترة شاملة لأي بيانات مفقودة (-999) من سيرفرات ناسا
      df = df[
          (df["Temp_C"] > -900)
          & (df["Rain_mm"] > -900)
          & (df["Soil_Moisture"] > -900)
          & (df["Evap_mm"] > -900)
      ].reset_index(drop=True)

      self.df = df
      return df

    except Exception as e:
      print(f"Error fetching data: {e}")
      return None

  def train_and_save_model(self):
    if self.df is None or self.df.empty:
      print("No data available to train.")
      return None

    features = ["Temp_C", "Rain_mm", "Soil_Moisture", "Evap_mm"]

    # 2. حساب حالة الإجهاد لكل يوم وإزاحتها لتوقع الغد (Early Warning System)
    actual_stress = np.where(
        (self.df["Temp_C"] > 26) & (self.df["Soil_Moisture"] < 0.4), 1, 0
    )
    self.df["Target_Tomorrow_Stress"] = pd.Series(actual_stress).shift(-1)

    # حذف آخر صف لأن ملوش بيانات لليوم التالي
    df_clean = self.df.dropna().copy()

    X = df_clean[features]
    y = df_clean["Target_Tomorrow_Stress"].astype(int)

    # تقسيم البيانات للتدريب والاختبار لقياس الدقة الفعلية
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # حساب دقة الموديل على بيانات لم يرها من قبل
    predictions = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, predictions)

    # 3. حفظ الموديل والـ Scaler على الجهاز للاستخدام الفوري لاحقاً
    joblib.dump(model, self.model_path)
    joblib.dump(scaler, self.scaler_path)
    print(f"Model trained & saved! Validation Accuracy: {acc * 100:.2f}%")
    return acc

  def predict_tomorrow_stress(self):
    if self.df is None or self.df.empty:
      return {"error": "No data available."}

    # لو الموديل مش متدرب قبل كده، دربه واحفظه تلقائياً
    if not os.path.exists(self.model_path) or not os.path.exists(
        self.scaler_path
    ):
      self.train_and_save_model()

    # تحميل الموديل الجاهز
    model = joblib.load(self.model_path)
    scaler = joblib.load(self.scaler_path)

    features = ["Temp_C", "Rain_mm", "Soil_Moisture", "Evap_mm"]

    # أخذ قراءة آخر يوم متاح للتنبؤ بحالة الغد
    latest_features = self.df[features].iloc[-1:]
    latest_scaled = scaler.transform(latest_features)

    prediction = model.predict(latest_scaled)[0]
    probability = model.predict_proba(latest_scaled)[0][1]

    return {
        "latest_date_analyzed": self.df["Date"].iloc[-1],
        "tomorrow_stress_predicted": bool(prediction),
        "stress_probability_percent": round(float(probability) * 100, 2),
        "total_clean_records": len(self.df),
    }


if __name__ == "__main__":
  # يفضل سحب سنتين أو تلاتة للتدريب عشان الموديل يشوف مواسم مختلفة بدقة أعلى
  processor = NASAAPIProcessor(
      lat=30.0444, lon=31.2357, start_date="20220101", end_date="20241231"
  )

  df = processor.fetch_data_from_nasa()
  if df is not None:
    print("\nData fetched successfully! Sample:")
    print(df.tail(3))

    # تدريب وحفظ الموديل (تقدر تشيل السطر ده لاحقاً لو عايز تستخدم المحفوظ مباشرة)
    processor.train_and_save_model()

    # التنبؤ بحالة الغد
    results = processor.predict_tomorrow_stress()
    print("\nEarly Warning Prediction for Tomorrow:")
    print(results)