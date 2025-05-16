from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
from train import train_model, preprocess_data

MODEL_PATH = "D:/fraud_detection_Ecommerce_project/model/fraud_model.pkl"
SCALER_PATH = "D:/fraud_detection_Ecommerce_project/model/scaler.pkl"
FEATURES_PATH = "D:/fraud_detection_Ecommerce_project/model/features.pkl"

def load_model_and_scaler():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    return model, scaler, feature_names

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    df = pd.read_csv(file_path)
    return jsonify({"message": "File uploaded successfully", "columns": df.columns.tolist(), "file_path": file_path})

@app.route("/train", methods=["POST"])
def train():
    file_path = request.json["file_path"]
    df = pd.read_csv(file_path)
    model, features = train_model(df)
    joblib.dump(features, "D:/fraud_detection_Ecommerce_project/model/features.pkl")
    return jsonify({"message": "Model trained successfully", "features": features[:15]})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        model, scaler, feature_names = load_model_and_scaler()
        data = request.json["input"]
        input_df = pd.DataFrame([data], columns=feature_names[:15])
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0][0]
        result = "Fraud" if prediction > 0.5 else "Not Fraud"
        return jsonify({"prediction": result, "probability": float(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
