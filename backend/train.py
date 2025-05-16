from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
from tensorflow.keras import Input
import pandas as pd
import numpy as np
import os
import joblib

import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend for safe thread usage
import matplotlib.pyplot as plt

MODEL_PATH = "D:/fraud_detection_Ecommerce_project/model/fraud_model.h5"
SCALER_PATH = "D:/fraud_detection_Ecommerce_project/model/scaler.pkl"
ENCODER_PATH = "D:/fraud_detection_Ecommerce_project/model/ohe_encoder.pkl"
FEATURES_PATH = "D:/fraud_detection_Ecommerce_project/model/selected_features.pkl"
ACCURACY_PLOT_PATH = "D:/fraud_detection_Ecommerce_project/model/accuracy_plot.png"
ROC_PLOT_PATH = "D:/fraud_detection_Ecommerce_project/model/roc_curve.png"

def preprocess_data(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def train_model(df, label_col):
    df = preprocess_data(df)
    label_col = label_col.strip().lower().replace(" ", "_")

    # Save all original columns
    joblib.dump(df.columns.tolist(), "D:/fraud_detection_Ecommerce_project/model/features.pkl")

    # Define selected input features
    selected_features = [
        "transaction_amount",
        "product_category",
        "customer_age",
        "account_age_days",
        "payment_method",
        "quantity",
        "device_used",
        "transaction_hour"
    ]
    joblib.dump(selected_features, FEATURES_PATH)

    # Split categorical and numerical
    categorical_cols = ["product_category", "payment_method", "device_used"]
    numerical_cols = [col for col in selected_features if col not in categorical_cols]

    X_categorical = df[categorical_cols]
    X_numerical = df[numerical_cols]
    y = df[label_col]

    # Encode categoricals
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_encoded = encoder.fit_transform(X_categorical)
    joblib.dump(encoder, ENCODER_PATH)

    # Combine numerical + encoded features
    X = np.concatenate([X_numerical.values, X_encoded], axis=1)

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, SCALER_PATH)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Build model
    model = Sequential([
        Input(shape=(X_train.shape[1],)),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'AUC'])

    # Train and capture history
    history = model.fit(
        X_train, y_train,
        epochs=20,
        batch_size=32,
        validation_data=(X_test, y_test),
        class_weight={0: 1, 1: 5},
        callbacks=[EarlyStopping(patience=3, restore_best_weights=True)]
    )

    # Save the model
    model.save(MODEL_PATH)

    os.makedirs(os.path.dirname(ACCURACY_PLOT_PATH), exist_ok=True)

    # Accuracy plot
    plt.figure(figsize=(8, 5))
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ACCURACY_PLOT_PATH)
    plt.close()

    # AUC-ROC plot
    y_pred_proba = model.predict(X_test).ravel()
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 5))
    plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.title('ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ROC_PLOT_PATH)
    plt.close()

    print(f"✅ Accuracy plot saved to: {ACCURACY_PLOT_PATH}")
    print(f"✅ ROC curve saved to: {ROC_PLOT_PATH}")
    print("🚀 Training completed successfully!")

    return model, selected_features
