from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ✅ FIXED IMPORT
from backend.app.services.ml_service import ml_service

router = APIRouter()

class PredictionRequest(BaseModel):
    district: str
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_direction: float
    cloud_cover: float
    rainfall_1h: Optional[float] = 0
    rainfall_3h: Optional[float] = 0

class PredictionResponse(BaseModel):
    district: str
    timestamp: datetime
    cloudburst_probability: float
    risk_level: str
    warning_hours: int
    message: str


@router.post("/predict", response_model=PredictionResponse)
def predict_cloudburst(request: PredictionRequest):

    features = {
        "temperature": request.temperature,
        "humidity": request.humidity,
        "pressure": request.pressure,
        "wind_speed": request.wind_speed,
        "cloud_cover": request.cloud_cover
    }

    probability = ml_service.predict(features)

    if probability > 0.7:
        risk = "HIGH"
        msg = "Immediate action required"
        hours = 2
    elif probability > 0.4:
        risk = "MEDIUM"
        msg = "Monitor closely"
        hours = 4
    else:
        risk = "LOW"
        msg = "Normal conditions"
        hours = 6

    return {
        "district": request.district,
        "timestamp": datetime.now(),
        "cloudburst_probability": round(probability * 100, 2),
        "risk_level": risk,
        "warning_hours": hours,
        "message": msg
    }
