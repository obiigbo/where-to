import os
from typing import Any, List, Union

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()


class WeatherInfo(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class MainWeatherData(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class WeatherResponse(BaseModel):
    coord: dict[str, float]
    weather: List[WeatherInfo]
    base: str
    main: MainWeatherData
    visibility: int
    wind: dict[str, float]
    clouds: dict[str, int]
    dt: int
    sys: dict[str, Any]
    timezone: int
    id: int
    name: str
    cod: int


class ErrorResponse(BaseModel):
    cod: int
    message: str


def get_current_weather(city: str = "London") -> Union[WeatherResponse, ErrorResponse]:
    request_url = f"http://api.openweathermap.org/data/2.5/weather?appid={os.getenv('API_KEY')}&q={city}&units=metric"

    weather_data = requests.get(request_url).json()

    try:
        if weather_data.get('cod') == 200:
            return WeatherResponse(**weather_data)
        else:
            return ErrorResponse(**weather_data)
    except ValidationError:
        return ErrorResponse(cod=500, message="Invalid response format")
