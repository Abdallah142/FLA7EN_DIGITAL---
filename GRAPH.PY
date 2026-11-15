import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# 1. جلب البيانات وتجهيزها
def get_nasa_data(lat=30.0444, lon=31.2357, start="20220101", end="20241231"):
  url = "https://power.larc.nasa.gov/api/temporal/daily/point"
  params = {
      "start": start,
      "end": end,
      "latitude": lat,
      "longitude": lon,
      "community": "ag",
      "parameters": "T2M,PRECTOTCORR,GWETTOP,EVPTRNS",
      "format": "JSON",
  }
  res = requests.get(url, params=params, timeout=15).json()
  props = res["properties"]["parameter"]
  dates = list(props["T2M"].keys())

  df = pd.DataFrame({
      "Temp_C": [props["T2M"][d] for d in dates],
      "Rain_mm": [props["PRECTOTCORR"][d] for d in dates],
      "Soil_Moisture": [props["GWETTOP"][d] for d in dates],
      "Evap_mm": [props["EVPTRNS"][d] for d in dates],
  })
  df = df[(df > -900).all(axis=1)].reset_index(drop=True)

  actual_stress = np.where(
      (df["Temp_C"] > 26) & (df["Soil_Moisture"] < 0.4), 1, 0
  )
  df["Target"] = pd.Series(actual_stress).shift(-1)
  return df.dropna()


print("Fetching NASA data & building Matplotlib visuals...")
df = get_nasa_data()

features = ["Temp_C", "Rain_mm", "Soil_Moisture", "Evap_mm"]
X = df[features]
y = df["Target"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

# 2. إعداد لوحة الرسم بـ Matplotlib
plt.style.use("dark_background")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.patch.set_facecolor("#0b1220")
fig.suptitle(
    "NASA POWER · Crop Stress Data & Model Analysis",
    fontsize=16,
    fontweight="bold",
    color="#e6edf7",
)

# --- الرسمة 1: توزيع الحرارة ورطوبة التربة ---
normal_days = df[df["Target"] == 0]
stress_days = df[df["Target"] == 1]

axes[0, 0].scatter(
    normal_days["Temp_C"],
    normal_days["Soil_Moisture"],
    c="#36c99a",
    alpha=0.6,
    label="Normal Day (0)",
    edgecolors="none",
)
axes[0, 0].scatter(
    stress_days["Temp_C"],
    stress_days["Soil_Moisture"],
    c="#ff5c5c",
    alpha=0.8,
    label="Stress Day (1)",
    edgecolors="none",
)
axes[0, 0].axvline(26, color="#f0a64a", linestyle="--", linewidth=1.2)
axes[0, 0].axhline(0.4, color="#f0a64a", linestyle="--", linewidth=1.2)
axes[0, 0].set_title("1. Data Distribution: Temperature vs Soil Moisture")
axes[0, 0].set_xlabel("Temperature (°C)")
axes[0, 0].set_ylabel("Surface Soil Moisture")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.15)

# --- الرسمة 2: أهمية العوامل في اتخاذ القرار ---
importances = model.feature_importances_ * 100
sorted_idx = np.argsort(importances)
bars = axes[0, 1].barh(
    [features[i] for i in sorted_idx],
    importances[sorted_idx],
    color="#4c8bf5",
    height=0.55,
)
axes[0, 1].set_title("2. Feature Importance (%)")
axes[0, 1].set_xlabel("Contribution to Prediction (%)")
axes[0, 1].set_xlim(0, max(importances) + 12)
axes[0, 1].grid(True, axis="x", alpha=0.15)

for bar in bars:
  width = bar.get_width()
  axes[0, 1].text(
      width + 1,
      bar.get_y() + bar.get_height() / 2,
      f"{width:.1f}%",
      va="center",
      color="#e6edf7",
      fontweight="bold",
  )

# --- الرسمة 3: مصفوفة الارتباك (Confusion Matrix) ---
cm = confusion_matrix(y_test, y_pred)
im = axes[1, 0].imshow(cm, cmap="Blues")
axes[1, 0].set_title("3. Confusion Matrix (Test Set)")
axes[1, 0].set_xticks([0, 1])
axes[1, 0].set_yticks([0, 1])
axes[1, 0].set_xticklabels(["Predicted Normal", "Predicted Stress"])
axes[1, 0].set_yticklabels(["Actual Normal", "Actual Stress"])

for i in range(2):
  for j in range(2):
    text_color = "white" if cm[i, j] > cm.max() / 2 else "black"
    axes[1, 0].text(
        j,
        i,
        str(cm[i, j]),
        ha="center",
        va="center",
        color=text_color,
        fontsize=14,
        fontweight="bold",
    )

# --- الرسمة 4: احتمالية الإجهاد على عينة من أيام الاختبار ---
sample_range = range(40)
axes[1, 1].plot(
    sample_range,
    y_test.values[:40],
    label="Actual Stress",
    color="#f0a64a",
    marker="o",
    linewidth=1.5,
)
axes[1, 1].plot(
    sample_range,
    y_prob[:40],
    label="AI Predicted Probability",
    color="#36c99a",
    linestyle="--",
    linewidth=2,
)
axes[1, 1].set_title("4. Actual vs Predicted Probability (40 Test Days)")
axes[1, 1].set_xlabel("Test Sample Index")
axes[1, 1].set_ylabel("Stress Probability (0 to 1)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.15)

for ax in axes.flat:
  ax.set_facecolor("#111c2e")

plt.tight_layout(rect=[0, 0.02, 1, 0.94])
plt.savefig("matplotlib_analysis.png", dpi=300, facecolor="#0b1220")
print("Saved high-res plot to 'matplotlib_analysis.png'")
plt.show()