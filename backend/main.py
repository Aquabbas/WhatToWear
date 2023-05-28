from fastapi import FastAPI
from pydantic import BaseModel
import requests


class UserPreferences(BaseModel):
    gender: str
    comfort_level: str

class WeatherData(BaseModel):
    temperature: float
    precipitation: float
    sky_conditions: str
    wind_conditions: str
    time_of_day: str
    humidity_level: float
    uv_levels: float

class ClothingItems(BaseModel):
    head: str
    face: str
    torso: str
    hands: str
    legs: str
    feet: str


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the WhatToWear API!"}


@app.get("/weather/{location}")
def get_weather(location: str):
    # Logic to fetch weather data from the WeatherKit API based on the provided location
    # Return the fetched weather data
    api_key = "YOUR_WEATHERKIT_API_KEY"  # Replace with your WeatherKit API key
    url = f"https://api.weatherkit.io/v2/weather?api_key={api_key}&location={location}"
    
    response = requests.get(url)
    weather_data = response.json()
    
    return weather_data


@app.post("/recommendation")
def send_recommendation(user_preferences: UserPreferences, weather_data: WeatherData):
    # Logic to generate clothing recommendations based on user preferences and weather data
    # Return the generated recommendations
    # Implement your recommendation logic here using the user_preferences and weather_data
    recommendation = {"outfit": "sweater, jeans, and boots"}  # Placeholder recommendation
    
    return recommendation


