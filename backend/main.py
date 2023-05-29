from fastapi import FastAPI
from pydantic import BaseModel

import requests
import os
from dotenv import load_dotenv

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder



# Load environment variables from .env file
load_dotenv()

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

class ClothingRecommendation:
    def __init__(self):
        self.model = RandomForestClassifier()  # Initialize the model

    def train_model(self, X, y):
        # Train the recommendation model
        self.model.fit(X, y)

    def generate_recommendation(self, weather_data, user_preferences):
        # Process the weather_data and user_preferences to generate recommendations
        # Implement the logic to analyze weather conditions and user preferences

        # Example: Generate a recommendation based on weather temperature
        if weather_data.temperature < 60:
            recommendation = "Wear a sweater or jacket."
        else:
            recommendation = "Wear a t-shirt or light clothing."

        return recommendation


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the WhatToWear API!"}


@app.get("/weather/{location}")
def get_weather(location: str):
    api_key = os.getenv("VISUAL_CROSSING_API_KEY")  # Retrieve API key from environment variable
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=us&key={api_key}"

    response = requests.get(url)
    response_content = response.text  # Use 'text' instead of 'content'

    print("Response Content:", response.content)
    print("Response Status Code:", response.status_code)

    if response.status_code == 200:
        try:
            weather_data = response.json()
            
            current_conditions = weather_data['currentConditions']
            forecast = weather_data['days'][0]['hours']

            # Extract and process current conditions data
            current_temp = current_conditions['temp']
            current_conditions_desc = current_conditions['conditions']
            current_icon = current_conditions['icon']

            # Extract and process forecast data
            hourly_forecast = []
            for hour in forecast:
                datetime = hour['datetime']
                temp = hour['temp']
                humidity = hour['humidity']
                conditions_desc = hour['conditions']
                icon = hour['icon']
                hourly_forecast.append({'datetime': datetime, 'temp': temp, 'humidity': humidity, 'conditions': conditions_desc, 'icon': icon})
            
            return {'current_conditions': current_conditions, 'forecast': hourly_forecast}
            
        except (KeyError, IndexError) as e:
            return {"error": "Failed to extract weather data from the API response."}

    else:
        return {"error": "Failed to retrieve weather data from the API."}


def parse_weather_data(data: dict) -> WeatherData:
    # Implement the parsing logic to extract relevant weather information from the data dictionary
    # and populate the WeatherData model
    # Example:
    temperature = data["currentConditions"]["temp"]
    precipitation = data["currentConditions"]["precip"]
    # Parse other weather attributes similarly
    weather_data = WeatherData(
        temperature=temperature,
        precipitation=precipitation,
        # Set other attributes accordingly
    )
    return weather_data


@app.post("/recommendation")
def send_recommendation(user_preferences: UserPreferences, weather_data: WeatherData):
    # Initialize the recommendation engine
    recommendation_engine = ClothingRecommendation()

    # Process user preferences and weather data if necessary
    # ...

    # Generate clothing recommendations
    recommendation = recommendation_engine.generate_recommendation(weather_data, user_preferences)

    return {"recommendation": recommendation}

