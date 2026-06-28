import streamlit as st

try:
    from utils.prediction import predict_irrigation
    from utils.llm import generate_explanation
except ModuleNotFoundError:
    from pages.utils.prediction import predict_irrigation
    from pages.utils.llm import generate_explanation

st.set_page_config(page_title="Prediction", page_icon="🌱", layout="wide")

if "prediction_state" not in st.session_state:
    st.session_state.prediction_state = {
        "has_run": False,
        "prediction_text": None,
        "confidence_value": None,
        "needs_irrigation": None,
        "explanation": None,
    }


def _build_input_payload(**kwargs):
    return {
        "Soil_Type": kwargs["soil_type"],
        "Soil_pH": kwargs["soil_ph"],
        "Soil_Moisture": kwargs["soil_moisture"],
        "Organic_Carbon": kwargs["organic_carbon"],
        "Electrical_Conductivity": kwargs["electrical_conductivity"],
        "Temperature_C": kwargs["temperature"],
        "Humidity": kwargs["humidity"],
        "Rainfall_mm": kwargs["rainfall"],
        "Sunlight_Hours": kwargs["sunlight"],
        "Wind_Speed_kmh": kwargs["wind_speed"],
        "Crop_Type": kwargs["crop_type"],
        "Crop_Growth_Stage": kwargs["crop_stage"],
        "Season": kwargs["season"],
        "Irrigation_Type": kwargs["irrigation_type"],
        "Water_Source": kwargs["water_source"],
        "Field_Area_hectare": kwargs["field_area"],
        "Mulching_Used": kwargs["mulching"],
        "Previous_Irrigation_mm": kwargs["previous_irrigation"],
        "Region": kwargs["region"],
    }


def _render_prediction_result(payload):
    st.markdown(f"<div class='result-box'><h3 style='margin:0 0 6px 0;'>🌿 Prediction Outcome</h3><p style='margin:0 0 6px 0;'><strong>{payload['prediction_text']}</strong></p><p style='margin:0;'>Confidence: <strong>{payload['confidence_value']:.2f}%</strong></p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h4 style='margin:0 0 8px 0;'>📈 Confidence</h4></div>", unsafe_allow_html=True)
    st.progress(float(payload["confidence_value"]) / 100)
    st.metric("Model Confidence", f"{payload['confidence_value']:.2f}%")

    st.markdown("<div class='card'><h4 style='margin:0 0 8px 0;'>🤖 AI Explanation</h4></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ai-explanation-card'>{payload['explanation']}</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h4 style='margin:0 0 8px 0;'>💧 Water Recommendations</h4></div>", unsafe_allow_html=True)
    rec1, rec2 = st.columns(2)
    with rec1:
        st.markdown("<div class='recommend-card'><h5 style='margin:0 0 6px 0;'>Save Water</h5><ul style='margin:0; padding-left:18px;'><li>Use drip irrigation where possible.</li><li>Irrigate early in the morning.</li><li>Check soil moisture before watering.</li></ul></div>", unsafe_allow_html=True)
    with rec2:
        st.markdown("<div class='recommend-card'><h5 style='margin:0 0 6px 0;'>Farm Practice</h5><ul style='margin:0; padding-left:18px;'><li>Monitor the weather forecast.</li><li>Maintain irrigation equipment.</li><li>Use mulch to reduce evaporation.</li></ul></div>", unsafe_allow_html=True)

    if payload["needs_irrigation"]:
        st.markdown("<div class='card'><strong>Irrigation is recommended</strong> based on the current field conditions and confidence score.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='card'><strong>Irrigation is not required right now.</strong> Continue monitoring soil moisture regularly.</div>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #f4fff4 0%, #eaf8ea 100%); }
    .block-container { padding-top: 0.4rem; padding-bottom: 1.4rem; }
    .card { background: white; color: #1f2937; border-radius: 16px; padding: 14px 16px; box-shadow: 0 6px 18px rgba(31, 83, 41, 0.08); margin-bottom: 12px; border: 1px solid #e4f3e4; }
    div.stButton > button { width: 100%; border-radius: 12px; background: linear-gradient(135deg, #2e7d32, #4caf50); border: none; color: white; font-weight: 700; }
    .result-box { background: linear-gradient(135deg, #eefbf0, #f8fff8); border-left: 4px solid #2e7d32; border-radius: 14px; padding: 14px; color: #1f2937; }
    .recommend-card { background: white; border: 1px solid #e4f3e4; border-radius: 14px; padding: 12px; color: #1f2937; }
    .ai-explanation-card { background: #ffffff; color: #111111; border: 1px solid #e4f3e4; border-radius: 16px; padding: 18px 20px; margin: 10px 0 12px; box-shadow: 0 8px 24px rgba(31, 83, 41, 0.11); font-size: 16px; line-height: 1.8; white-space: pre-wrap; }
    .ai-explanation-card h1, .ai-explanation-card h2, .ai-explanation-card h3, .ai-explanation-card h4, .ai-explanation-card h5, .ai-explanation-card h6 { color: #1b5e20; margin: 0 0 8px 0; font-weight: 700; }
    .ai-explanation-card p, .ai-explanation-card li, .ai-explanation-card strong { color: #111111; }
    .ai-explanation-card p { margin: 0 0 10px 0; }
    .ai-explanation-card ul { padding-left: 20px; margin: 0 0 10px 0; }
    .ai-explanation-card strong { color: #1b5e20; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='card'><h2 style='margin:0 0 6px 0;'>Irrigation Prediction</h2><p style='margin:0; color:#4b5563;'>Enter field conditions and receive a compact, data-driven recommendation.</p></div>", unsafe_allow_html=True)

left, right = st.columns([1.1, 0.9], gap="small")
with left:
    st.markdown("<div class='card'><h4 style='margin:0 0 8px 0;'>🌾 Soil & Weather</h4></div>", unsafe_allow_html=True)
    soil_type = st.selectbox("Soil Type", ["Clay", "Loamy", "Sandy", "Silt"])
    soil_ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=7.0)
    soil_moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=45.0)
    organic_carbon = st.number_input("Organic Carbon", value=0.5)
    electrical_conductivity = st.number_input("Electrical Conductivity", value=1.0)
    temperature = st.number_input("Temperature (°C)", value=28.0)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=65.0)
    rainfall = st.number_input("Rainfall (mm)", value=20.0)
    sunlight = st.number_input("Sunlight Hours", value=8.0)
    wind_speed = st.number_input("Wind Speed (km/h)", value=12.0)

with right:
    st.markdown("<div class='card'><h4 style='margin:0 0 8px 0;'>🌱 Crop & Farm Context</h4></div>", unsafe_allow_html=True)
    crop_type = st.selectbox("Crop Type", ["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Wheat"])
    crop_stage = st.selectbox("Crop Growth Stage", ["Flowering", "Harvest", "Sowing", "Vegetative"])
    season = st.selectbox("Season", ["Kharif", "Rabi", "Zaid"])
    irrigation_type = st.selectbox("Irrigation Type", ["Canal", "Drip", "Rainfed", "Sprinkler"])
    water_source = st.selectbox("Water Source", ["Groundwater", "Rainwater", "Reservoir", "River"])
    field_area = st.number_input("Field Area (hectare)", value=1.0)
    mulching = st.selectbox("Mulching Used", ["No", "Yes"])
    previous_irrigation = st.number_input("Previous Irrigation (mm)", value=10.0)
    region = st.selectbox("Region", ["Central", "East", "North", "South", "West"])

predict = st.button("🌱 Predict Irrigation", use_container_width=True)

if predict:
    input_data = _build_input_payload(
        soil_type=soil_type,
        soil_ph=soil_ph,
        soil_moisture=soil_moisture,
        organic_carbon=organic_carbon,
        electrical_conductivity=electrical_conductivity,
        temperature=temperature,
        humidity=humidity,
        rainfall=rainfall,
        sunlight=sunlight,
        wind_speed=wind_speed,
        crop_type=crop_type,
        crop_stage=crop_stage,
        season=season,
        irrigation_type=irrigation_type,
        water_source=water_source,
        field_area=field_area,
        mulching=mulching,
        previous_irrigation=previous_irrigation,
        region=region,
    )

    try:
        with st.spinner("Loading prediction model..."):
            prediction, confidence = predict_irrigation(input_data)
        prediction_text = str(prediction).strip()
        needs_irrigation = str(prediction_text).lower() in ["yes", "required", "irrigation required", "1"]
        confidence_value = float(confidence or 0.0)

        with st.spinner("Generating AI explanation..."):
            explanation = generate_explanation(
                prediction=prediction_text,
                soil_moisture=soil_moisture,
                temperature=temperature,
                humidity=humidity,
                rainfall=rainfall,
                confidence=confidence_value,
                crop_type=crop_type,
                crop_stage=crop_stage,
                season=season,
                irrigation_type=irrigation_type,
                water_source=water_source,
                soil_ph=soil_ph,
                organic_carbon=organic_carbon,
                electrical_conductivity=electrical_conductivity,
                sunlight_hours=sunlight,
                wind_speed=wind_speed,
                field_area=field_area,
                mulching=mulching,
                previous_irrigation=previous_irrigation,
                region=region,
            )

        st.session_state.prediction_state = {
            "has_run": True,
            "prediction_text": prediction_text,
            "confidence_value": confidence_value,
            "needs_irrigation": needs_irrigation,
            "explanation": explanation,
        }
        _render_prediction_result(st.session_state.prediction_state)
    except Exception as exc:
        st.session_state.prediction_state = {"has_run": False, "prediction_text": None, "confidence_value": None, "needs_irrigation": None, "explanation": None}
        st.error(f"Prediction failed: {exc}")
elif st.session_state.prediction_state.get("has_run"):
    _render_prediction_result(st.session_state.prediction_state)
