from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Cloudburst Prediction System",
    description="Real-time cloudburst prediction",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIXED IMPORTS
from backend.app.api import weather, prediction, historical, mosdac, imd, auth

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(prediction.router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(historical.router, prefix="/api/historical", tags=["Historical"])
app.include_router(mosdac.router, prefix="/api/mosdac", tags=["MOSDAC"])
app.include_router(imd.router, prefix="/api/imd", tags=["IMD"])

@app.get("/")
def root():
    return {"message": "Cloudburst API running"}

@app.get("/health")
def health():
    return {"status": "ok"}
