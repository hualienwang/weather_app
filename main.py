import os
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from weather_client import WeatherClient
from auth import verify_api_key
from database import init_db, get_top_cities
from dotenv import load_dotenv

load_dotenv()
init_db()

try:
    weather_client = WeatherClient()
except Exception as e:
    weather_client = None

app = FastAPI(
    title="🌤️ 天氣 API 2.1",
    description="支援 API Key 認證的天氣服務",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/register")
async def register_api_key(owner: str = "anonymous"):
    from database import create_api_key
    key = create_api_key(owner)
    return {"api_key": key, "owner": owner}

@app.get("/weather/current/{city}")
async def get_current_weather(
    city: str,
    request: Request,
    api_key_id: int = Depends(verify_api_key)
):
    if not weather_client:
        raise HTTPException(500, "天氣服務未初始化")
    ip = request.client.host if request.client else "unknown"
    try:
        data = weather_client.get_current(city)
        from database import log_query
        log_query(city.lower(), ip, data["icon_code"], api_key_id)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(500, f"天氣查詢失敗: {e}")

@app.get("/weather/forecast/{city}")
async def get_forecast(
    city: str,
    request: Request,
    api_key_id: int = Depends(verify_api_key)
):
    if not weather_client:
        raise HTTPException(500, "天氣服務未初始化")
    try:
        data = weather_client.get_forecast(city, days=3)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(500, f"預報查詢失敗: {e}")

@app.get("/stats/top-cities")
async def top_cities(api_key_id: int = Depends(verify_api_key)):
    try:
        stats = get_top_cities(days=7)
        return {"status": "success", "data": stats}
    except Exception as e:
        raise HTTPException(500, f"統計失敗: {e}")

@app.get("/")
async def root():
    return {"message": "🌤️ 天氣 API 2.1", "docs": "/docs"}