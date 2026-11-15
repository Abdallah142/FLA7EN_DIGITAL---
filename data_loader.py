import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class DirectFarmProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_and_clean_data(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        ext = os.path.splitext(self.file_path)[1].lower()

        if ext == '.csv':
            self.df = pd.read_csv(self.file_path)
        elif ext in ['.xls', '.xlsx']:
            self.df = pd.read_excel(self.file_path)
        elif ext == '.json':
            self.df = pd.read_json(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

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

    def run_ai_model(self):
        if self.df is None or self.df.empty:
            return "No data available to run AI model."

        expected_features = ['temp_c', 'rain_mm', 'soil_moisture', 'evap_mm']
        
        for feat in expected_features:
            if feat not in self.df.columns:
                return f"Error: Required column '{feat}' not found in your dataset. Please check column names."

        X = self.df[expected_features]
        
        if 'high_stress' in self.df.columns:
            y = self.df['high_stress']
        else:
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
            "total_rows_processed": len(self.df)
        }

if __name__ == "__main__":
    
    file_path = "dataset.csv" 
    
    print(f"Loading and processing data from: {file_path}")
    
    processor = DirectFarmProcessor(file_path)
    clean_data = processor.load_and_clean_data()
    
    print("\nData loaded and cleaned successfully! First 3 rows:")
    print(clean_data.head(3))
    
    print("\nRunning AI prediction model...")
    results = processor.run_ai_model()
    
    print("\nAI Model Results:")
    print(results)