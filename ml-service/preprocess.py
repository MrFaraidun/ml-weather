import pandas as pd
import numpy as np
import os
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

DATA_URL = "https://rattle.togaware.com/weatherAUS.csv"
DATA_PATH = "../data/weatherAUS.csv"
PROCESSED_DATA_PATH = "../data/processed_data.joblib"

def download_data():
    if not os.path.exists(DATA_PATH):
        print(f"Downloading dataset from {DATA_URL}...")
        response = requests.get(DATA_URL)
        with open(DATA_PATH, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("Dataset already exists.")

def preprocess_data():
    download_data()
    
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    # Drop columns with too many missing values or irrelevant ones
    # RISK_MM is often dropped in this dataset as it's a proxy for the target
    cols_to_drop = ['Date', 'Location', 'RISK_MM']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    # Drop rows where target is missing
    df = df.dropna(subset=['RainTomorrow'])
    
    # Separate features and target
    X = df.drop('RainTomorrow', axis=1)
    y = df['RainTomorrow']
    
    # Handle missing values
    # For numerical columns, use median
    num_cols = X.select_dtypes(include=['float64', 'int64']).columns
    X[num_cols] = X[num_cols].fillna(X[num_cols].median())
    
    # For categorical columns, use mode
    cat_cols = X.select_dtypes(include=['object']).columns
    for col in cat_cols:
        X[col] = X[col].fillna(X[col].mode()[0])
    
    # Encode categorical features
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
    
    # Encode target
    le_target = LabelEncoder()
    y = le_target.fit_transform(y.astype(str))
    encoders['RainTomorrow'] = le_target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale numerical features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save everything
    processed_data = {
        'X_train': X_train_scaled,
        'X_test': X_test_scaled,
        'y_train': y_train,
        'y_test': y_test,
        'feature_names': X.columns.tolist(),
        'encoders': encoders,
        'scaler': scaler
    }
    
    print(f"Saving processed data to {PROCESSED_DATA_PATH}...")
    joblib.dump(processed_data, PROCESSED_DATA_PATH)
    print("Preprocessing complete.")
    
    return processed_data

if __name__ == "__main__":
    preprocess_data()
