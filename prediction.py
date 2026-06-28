import os
import joblib
import numpy as np
import streamlit as st

# ==========================
# Paths
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODELS_DIR, "best_model.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
TARGET_ENCODER_PATH = os.path.join(MODELS_DIR, "label_encoder.pkl")
FEATURE_ENCODERS_PATH = os.path.join(MODELS_DIR, "feature_encoders.pkl")

FEATURE_COLUMNS = [
    "Soil_Type",
    "Soil_pH",
    "Soil_Moisture",
    "Organic_Carbon",
    "Electrical_Conductivity",
    "Temperature_C",
    "Humidity",
    "Rainfall_mm",
    "Sunlight_Hours",
    "Wind_Speed_kmh",
    "Crop_Type",
    "Crop_Growth_Stage",
    "Season",
    "Irrigation_Type",
    "Water_Source",
    "Field_Area_hectare",
    "Mulching_Used",
    "Previous_Irrigation_mm",
    "Region",
]

CATEGORICAL_COLUMNS = [
    "Soil_Type",
    "Crop_Type",
    "Crop_Growth_Stage",
    "Season",
    "Irrigation_Type",
    "Water_Source",
    "Mulching_Used",
    "Region",
]


@st.cache_resource(show_spinner=False)
def load_model_bundle():
    model = None
    scaler = None
    target_encoder = None
    feature_encoders = {}

    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    if os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
    if os.path.exists(TARGET_ENCODER_PATH):
        target_encoder = joblib.load(TARGET_ENCODER_PATH)
    if os.path.exists(FEATURE_ENCODERS_PATH):
        feature_encoders = joblib.load(FEATURE_ENCODERS_PATH)

    return model, scaler, target_encoder, feature_encoders

# ==========================
# Encode Categorical Features
# ==========================


def _coerce_numeric(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def encode_features(data, feature_encoders):
    encoded = data.copy()

    for col in CATEGORICAL_COLUMNS:
        if col in feature_encoders and col in encoded:
            try:
                encoded[col] = feature_encoders[col].transform([encoded[col]])[0]
            except Exception:
                encoded[col] = -1

    return encoded


# ==========================
# Prediction Function
# ==========================

def predict_irrigation(input_data):
    model, scaler, target_encoder, feature_encoders = load_model_bundle()
    if model is None or scaler is None:
        raise RuntimeError("Required model files were not found. Prediction cannot run right now.")

    encoded_data = encode_features(input_data, feature_encoders)
    values = np.array([_coerce_numeric(encoded_data.get(col, 0)) for col in FEATURE_COLUMNS], dtype=float).reshape(1, -1)

    values = scaler.transform(values) if hasattr(scaler, "transform") else values

    prediction = model.predict(values)
    confidence = None

    if hasattr(model, "predict_proba"):
        confidence = np.max(model.predict_proba(values)) * 100

    if target_encoder is not None:
        prediction = target_encoder.inverse_transform(prediction)

    return prediction[0], confidence