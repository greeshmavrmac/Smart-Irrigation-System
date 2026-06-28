import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ENV_PATHS = [BASE_DIR / ".env", BASE_DIR.parent / ".env", Path.cwd() / ".env"]

for env_path in ENV_PATHS:
    if env_path.exists():
        load_dotenv(env_path)
        break

try:
    from utils.prompts import SYSTEM_PROMPT, irrigation_prompt
except ModuleNotFoundError:
    from pages.utils.prompts import SYSTEM_PROMPT, irrigation_prompt


@st.cache_resource(show_spinner=False)
def create_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception:
        return None


client = create_client()


def _build_local_explanation(prediction, soil_moisture, temperature, humidity, rainfall, confidence=None, **kwargs):
    crop_type = str(kwargs.get("crop_type") or "the selected crop").strip()
    crop_stage = str(kwargs.get("crop_stage") or "the current stage").strip()
    season = str(kwargs.get("season") or "the current season").strip()
    irrigation_type = str(kwargs.get("irrigation_type") or "the selected method").strip()
    water_source = str(kwargs.get("water_source") or "the selected source").strip()

    soil_moisture_value = float(soil_moisture)
    temperature_value = float(temperature)
    humidity_value = float(humidity)
    rainfall_value = float(rainfall)
    confidence_value = float(confidence or 0)
    sunlight_hours = float(kwargs.get("sunlight_hours") or 0)
    wind_speed = float(kwargs.get("wind_speed") or 0)
    field_area = float(kwargs.get("field_area") or 1)

    moisture_low = soil_moisture_value < 35
    hot = temperature_value > 30
    wet = rainfall_value > 20 or humidity_value > 75
    windy = wind_speed > 18
    high_evaporation = (hot and sunlight_hours > 8) or windy

    if confidence_value < 70:
        summary = f"The model predicts {prediction}, but confidence is {confidence_value:.0f}%, so field verification should come before irrigation."
        urgency = "High"
        method = irrigation_type
        timing = "early morning after a quick field check"
        water_requirement = "a light to moderate dose based on a fresh soil check"
    elif moisture_low and hot:
        summary = f"The model predicts {prediction}, and the field is losing moisture quickly because soil moisture is low and temperature is high."
        urgency = "High"
        method = irrigation_type
        timing = "early morning"
        water_requirement = f"about {max(8, int(field_area * 12))} to {max(12, int(field_area * 16))} mm for this area"
    elif wet and soil_moisture_value > 50:
        summary = f"The model predicts {prediction}, but current rainfall and humidity already support the field, so irrigation can likely be delayed."
        urgency = "Low"
        method = irrigation_type
        timing = "after the next dry window"
        water_requirement = "only a small amount if the soil dries quickly"
    else:
        summary = f"The model predicts {prediction}, and the present field conditions need a measured decision rather than a rushed watering action."
        urgency = "Medium"
        method = irrigation_type
        timing = "early morning"
        water_requirement = f"about {max(6, int(field_area * 10))} to {max(10, int(field_area * 14))} mm depending on soil check"

    field_analysis = f"Soil moisture is {soil_moisture_value:.0f}% with {temperature_value:.0f}°C temperature, {humidity_value:.0f}% humidity, {rainfall_value:.0f} mm rainfall, {sunlight_hours:.0f} hours of sunlight and {wind_speed:.0f} km/h wind, so the field is {('drying fast' if high_evaporation else 'remaining moist' if wet else 'near balance')}."
    crop_analysis = f"{crop_type} at {crop_stage} in {season} is under {('strong water stress' if moisture_low and hot else 'reduced pressure' if wet else 'moderate demand')} because this growth stage and season influence water use."

    if urgency == "High":
        risk_analysis = "If irrigation is delayed, the crop may show stress and growth may slow; if irrigation is excessive, roots may suffer and water may be wasted."
    elif urgency == "Low":
        risk_analysis = "If irrigation is delayed, the field may remain wet longer than needed; if irrigation is excessive, runoff and water loss may increase."
    else:
        risk_analysis = "If irrigation is delayed, stress may rise; if irrigation is excessive, soil oxygen may drop and roots may struggle."

    water_conservation = (
        f"Use {method.lower()} irrigation only when the soil still feels dry, keep the field covered with mulch where possible, and adjust watering to the next weather window."
    )
    actions = [
        "Check soil moisture at sunrise.",
        "Inspect the irrigation line and emitters.",
        "Review the rain forecast for the next day.",
        "Confirm the crop looks stable before watering.",
        "Record the field condition for the next check.",
    ]

    return (
        f"AI Irrigation Analysis\n{summary}\n\n"
        f"Field Condition Analysis\n{field_analysis}\n\n"
        f"Crop Condition Analysis\n{crop_analysis}\n\n"
        f"LLM Recommendation\nIrrigation should be {'done now' if urgency == 'High' else 'postponed' if urgency == 'Low' else 'reviewed soon'}. Use {method.lower()} irrigation at {timing}.\n\n"
        f"Best Irrigation Strategy\nUrgency is {urgency.lower()} and the estimated water requirement is {water_requirement}.\n\n"
        f"Risk Analysis\n{risk_analysis}\n\n"
        f"Water Conservation Strategy\n{water_conservation}\n\n"
        f"Farmer Action Plan\n{actions[0]} {actions[1]} {actions[2]} {actions[3]} {actions[4]}"
    )


def generate_explanation(prediction, soil_moisture, temperature, humidity, rainfall, **kwargs):
    """Generate a compact explanation for the current prediction using local logic or Groq when available."""

    client = create_client()
    if client is None:
        return _build_local_explanation(
            prediction,
            soil_moisture,
            temperature,
            humidity,
            rainfall,
            confidence=kwargs.get("confidence"),
            **kwargs,
        )

    prompt = irrigation_prompt(
        prediction,
        soil_moisture,
        temperature,
        humidity,
        rainfall,
        confidence=kwargs.get("confidence"),
        crop_type=kwargs.get("crop_type"),
        crop_stage=kwargs.get("crop_stage"),
        season=kwargs.get("season"),
        irrigation_type=kwargs.get("irrigation_type"),
        water_source=kwargs.get("water_source"),
        soil_ph=kwargs.get("soil_ph"),
        organic_carbon=kwargs.get("organic_carbon"),
        electrical_conductivity=kwargs.get("electrical_conductivity"),
        sunlight_hours=kwargs.get("sunlight_hours"),
        wind_speed=kwargs.get("wind_speed"),
        field_area=kwargs.get("field_area"),
        mulching=kwargs.get("mulching"),
        previous_irrigation=kwargs.get("previous_irrigation"),
        region=kwargs.get("region"),
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.25,
        )
        content = response.choices[0].message.content.strip()
        return content or _build_local_explanation(
            prediction,
            soil_moisture,
            temperature,
            humidity,
            rainfall,
            confidence=kwargs.get("confidence"),
            **kwargs,
        )
    except Exception:
        return _build_local_explanation(
            prediction,
            soil_moisture,
            temperature,
            humidity,
            rainfall,
            confidence=kwargs.get("confidence"),
            **kwargs,
        )


def farmer_chat(question):
    """Agriculture chatbot."""

    if client is None:
        return "The AI assistant is unavailable because the Groq API key is not configured."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception:
        return "The AI service is temporarily unavailable. Please try again in a moment."