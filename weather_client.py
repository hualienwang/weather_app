import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class WeatherClient:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENWEATHER_API_KEY 未設定")
        self.current_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

    def _request(self, url, params):
        params.update({
            'appid': self.api_key,
            'lang': 'zh_tw',
            'units': 'metric'
        })
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_current(self, city: str):
        data = self._request(self.current_url, {'q': city})
        icon_code = data['weather'][0]['icon']
        return {
            "location": f"{data['name']}, {data['sys']['country']}",
            "temperature": round(data['main']['temp'], 1),
            "feels_like": round(data['main']['feels_like'], 1),
            "description": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "icon_code": icon_code,
            "icon_url": f"http://openweathermap.org/img/wn/{icon_code}@2x.png",
            "timestamp": datetime.fromtimestamp(data['dt']).isoformat()
        }

    def get_forecast(self, city: str, days: int = 3):
        data = self._request(self.forecast_url, {'q': city})
        forecasts = []
        seen_dates = set()
        for item in data['list']:
            if len(forecasts) >= days:
                break
            dt = datetime.fromtimestamp(item['dt'])
            date_str = dt.strftime('%Y-%m-%d')
            if date_str in seen_dates:
                continue
            hour_diff = abs(dt.hour - 12)
            if hour_diff <= 3:
                icon_code = item['weather'][0]['icon']
                forecasts.append({
                    "date": date_str,
                    "time": dt.strftime('%H:%M'),
                    "temperature": round(item['main']['temp'], 1),
                    "description": item['weather'][0]['description'],
                    "humidity": item['main']['humidity'],
                    "icon_url": f"http://openweathermap.org/img/wn/{icon_code}.png"
                })
                seen_dates.add(date_str)
        return forecasts