from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
import json
import tensorflow as tf
from threading import Thread
import models

app = Flask(__name__)
CORS(app)

MODELS_DIR = "../data/models"
RESULTS_PATH = "../data/model_results.json"
PROCESSED_DATA_PATH = "../data/processed_data.joblib"

# Global state for training status
training_status = {"status": "idle", "message": "Ready"}

def load_metadata():
    if os.path.exists(PROCESSED_DATA_PATH):
        data_meta = joblib.load(PROCESSED_DATA_PATH)
        return data_meta['encoders'], data_meta['scaler'], data_meta['feature_names']
    return {}, None, []

encoders, scaler, feature_names = load_metadata()

@app.route('/results', methods=['GET'])
def get_results():
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH, 'r') as f:
            results = json.load(f)
        return jsonify(results)
    return jsonify({"error": "Results not found. Please train models first."}), 404

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(training_status)

@app.route('/train', methods=['POST'])
def trigger_training():
    global training_status
    if training_status["status"] == "running":
        return jsonify({"error": "Training already in progress"}), 400
    
    def training_task():
        global training_status
        training_status = {"status": "running", "message": "Deep Training in progress..."}
        try:
            models.run_training()
            training_status = {"status": "idle", "message": "Training Completed Successfully"}
        except Exception as e:
            training_status = {"status": "error", "message": str(e)}

    Thread(target=training_task).start()
    return jsonify({"message": "Training started in background"}), 202

@app.route('/predict', methods=['POST'])
def predict():
    if not os.path.exists(RESULTS_PATH):
        return jsonify({"error": "Models not trained"}), 400

    input_data = request.json
    df_input = pd.DataFrame([input_data])
    
    # Reload metadata in case it changed
    global encoders, scaler, feature_names
    if not scaler:
        encoders, scaler, feature_names = load_metadata()

    for col, encoder in encoders.items():
        if col in df_input.columns and col != 'RainTomorrow':
            try:
                df_input[col] = encoder.transform(df_input[col].astype(str))
            except:
                df_input[col] = 0 

    for col in feature_names:
        if col not in df_input.columns:
            df_input[col] = 0
    df_input = df_input[feature_names]
    
    input_scaled = scaler.transform(df_input)
    
    with open(RESULTS_PATH, 'r') as f:
        results = json.load(f)
    best_info = max(results, key=lambda x: x['metrics']['accuracy'])
    model_name = best_info['model'].lower().replace(' ', '_')
    
    if model_name == 'ann':
        model = tf.keras.models.load_model(os.path.join(MODELS_DIR, 'ann.keras'))
        pred_prob = model.predict(input_scaled)
        prediction = int(pred_prob[0][0] > 0.5)
        probability = float(pred_prob[0][0])
    else:
        model = joblib.load(os.path.join(MODELS_DIR, f"{model_name}.joblib"))
        prediction = int(model.predict(input_scaled)[0])
        probability = float(model.predict_proba(input_scaled)[0][1]) if hasattr(model, "predict_proba") else None

    target_encoder = encoders['RainTomorrow']
    result = {
        'prediction': target_encoder.inverse_transform([prediction])[0],
        'probability': probability,
        'model_used': best_info['model']
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
