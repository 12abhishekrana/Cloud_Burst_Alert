from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# ---------------- APP INIT ----------------
app = FastAPI(
    title="Cloudburst Prediction System",
    description="Real-time cloudburst prediction for Uttarakhand, Himachal Pradesh & Jammu & Kashmir",
    version="2.0.0"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- IMPORT ROUTERS ----------------
# IMPORTANT: always use backend.app.*
from backend.app.api import (
    weather,
    prediction,
    historical,
    mosdac,
    imd,
    auth
)

# ---------------- INCLUDE ROUTERS ----------------
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(prediction.router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(historical.router, prefix="/api/historical", tags=["Historical"])
app.include_router(mosdac.router, prefix="/api/mosdac", tags=["MOSDAC"])
app.include_router(imd.router, prefix="/api/imd", tags=["IMD"])


# ---------------- ROOT ENDPOINT ----------------
@app.get("/")
async def root():
    return {
        "message": "CloudAlert API - Cloudburst Prediction System",
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "weather": "/api/weather",
            "prediction": "/api/prediction",
            "historical": "/api/historical",
            "mosdac": "/api/mosdac",
            "imd": "/api/imd"
        }
    }


# ---------------- HEALTH CHECK ----------------
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# ---------------- DEBUG ROUTES ----------------
@app.get("/routes")
async def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "methods": list(route.methods) if route.methods else []
        })
    return {"total_routes": len(routes), "routes": routes}
