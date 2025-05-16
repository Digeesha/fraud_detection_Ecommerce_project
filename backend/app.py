from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
import threading
from train import train_model, preprocess_data
from tensorflow.keras.models import load_model

# === File Paths ===
BASE_PATH = "D:/fraud_detection_Ecommerce_project/model"
MODEL_PATH = os.path.join(BASE_PATH, "fraud_model.h5")
SCALER_PATH = os.path.join(BASE_PATH, "scaler.pkl")
ENCODER_PATH = os.path.join(BASE_PATH, "ohe_encoder.pkl")
FEATURES_PATH = os.path.join(BASE_PATH, "selected_features.pkl")

# === Global Training Status ===
training_status = {"in_progress": False}

# === Load Model Function ===
def load_model_and_scaler():
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    encoder = joblib.load(ENCODER_PATH)
    features = joblib.load(FEATURES_PATH)
    return model, scaler, encoder, features

# === Flask App Setup ===
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Upload CSV ===
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    file_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, file.filename))
    file.save(file_path)
    df = pd.read_csv(file_path)
    return jsonify({
        "message": "File uploaded successfully",
        "columns": df.columns.tolist(),
        "file_path": file_path
    })

# === Train Model (Threaded) ===
@app.route("/train", methods=["POST"])
def train():
    data = request.json
    file_path = os.path.normpath(data.get("file_path"))
    label_col = "Is Fraudulent"

    # ✅ Set status BEFORE starting thread
    training_status["in_progress"] = True

    def background_training():
        try:
            df = pd.read_csv(file_path)
            if label_col not in df.columns:
                print(f"❌ Column '{label_col}' not found in file.")
                return
            model, features = train_model(df, label_col)
            print("✅ Training completed. Features:", features)
        except Exception as e:
            print("❌ Training failed:", str(e))
        finally:
            training_status["in_progress"] = False

    threading.Thread(target=background_training).start()
    return jsonify({"message": "✅ Training started in background."})


# === Check Training Status ===
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"training": training_status["in_progress"]})

# === Predict Endpoint ===
@app.route("/predict", methods=["POST"])
def predict():
    try:
        model, scaler, encoder, selected_features = load_model_and_scaler()
        data = request.json["input"]

        # DataFrame
        input_df = pd.DataFrame([data], columns=selected_features)

        # Split columns
        categorical_cols = ["product_category", "payment_method", "device_used"]
        numerical_cols = [col for col in selected_features if col not in categorical_cols]

        # Transform input
        input_cat = encoder.transform(input_df[categorical_cols])
        input_num = input_df[numerical_cols].values
        final_input = np.concatenate([input_num, input_cat], axis=1)
        final_scaled = scaler.transform(final_input)

        # Predict
        prediction = model.predict(final_scaled)[0][0]
        result = "Fraud" if prediction > 0.5 else "Not Fraud"
        return jsonify({
            "prediction": result,
            "probability": float(prediction)
        })

    except Exception as e:
        print("❌ Prediction error:", str(e))
        return jsonify({"error": str(e)}), 500

# === Run Server ===
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

