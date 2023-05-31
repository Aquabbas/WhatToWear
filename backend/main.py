from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import random

from pydantic import BaseModel
from typing import Optional

from dotenv import load_dotenv
import requests
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Download NLTK resources outside of the class
nltk.download('punkt')  # Tokenizer resource
nltk.download('averaged_perceptron_tagger')  # Part-of-speech tagger resource

from conversational_flow import conversational_flow

# Load environment variables from .env file
load_dotenv()



class UserPreferences(BaseModel):
    gender: str
    comfort_level: str


class WeatherData(BaseModel):
    temperature: float
    precipitation_probability: float
    precipitation: float
    cloudcover: float
    conditions: str
    windgust: Optional[float]
    windspeed: float
    uvindex: float
    humidity: float


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

        
        # Step 1: Check the gender of the runner and provide general recommendations
        if user_preferences.gender == "male":
            recommendation = "T-shirt, shorts, and running shoes."
        elif user_preferences.gender == "female":
            recommendation = "Tank top, shorts or leggings, and running shoes."
        else:
            recommendation = "Invalid gender."

        # Step 2: Adjust clothing choices based on comfort level
        if user_preferences.comfort_level == "low":
            recommendation += " Add additional layers for comfort."
        elif user_preferences.comfort_level == "mid":
            recommendation += " Dress comfortably for your run."
        elif user_preferences.comfort_level == "high":
            recommendation += " Dress lightly for your run."
        else:
            recommendation += " Invalid comfort level."
        
        # Step 3: Consider temperature and provide appropriate recommendations
        if weather_data.temperature < 40:
            recommendation += " Add layers like a long-sleeve shirt, running tights, and a lightweight jacket."
        elif 40 <= weather_data.temperature < 60:
            recommendation += " Wear a long-sleeve shirt and lightweight pants or leggings."
        elif 60 <= weather_data.temperature < 70:
            recommendation += " Wear a short-sleeve shirt and shorts or capris."
        elif weather_data.temperature >= 70:
            recommendation += " Wear a lightweight tank top and shorts."

        # Step 4: Consider precipitation amount and probability
        if weather_data.precipitation_probability > 50 and weather_data.precipitation > 0.1:
            recommendation += " Wear a waterproof or water-resistant jacket and pants."
        elif weather_data.precipitation_probability < 50 and weather_data.precipitation == 0:
            recommendation += " No specific rain gear is necessary."
        
        # Step 5: Consider cloud coverage and adjust clothing choices accordingly
        if weather_data.cloudcover > 70 and "overcast" in weather_data.conditions.lower():
            recommendation += " Wear additional layers to stay warm."
        elif weather_data.cloudcover < 70 and ("clear" in weather_data.conditions.lower() or "partly cloudy" in weather_data.conditions.lower()):
            recommendation += " Adjust clothing choices according to the weather."

        # Step 6: Consider wind speed and gust speed
        if weather_data.windgust is not None and (weather_data.windgust > 20 or weather_data.windspeed > 15):
            recommendation += " Wear a wind-resistant jacket or layer to protect against wind chill."
        
        # Step 7: Consider humidity and provide recommendations
        if weather_data.humidity > 70:
            recommendation += " Wear moisture-wicking clothing to stay comfortable and avoid excessive sweating."

        # Step 8: Consider UV index and provide recommendations
        if weather_data.uvindex > 7:
            recommendation += " Wear sunscreen, a hat, and sunglasses to protect against sunburn and excessive sun exposure."
        
        return recommendation


def parse_weather_data(data: dict) -> WeatherData:
    # Implement the parsing logic to extract relevant weather information from the data dictionary
    # and populate the WeatherData model
    # Example:
    temperature = data["currentConditions"]["temp"]
    precipitation = data["currentConditions"]["precip"]
    precipitation_probability = data["currentConditions"]["precipprob"]
    cloudcover = data["currentConditions"]["cloudcover"]
    conditions = data["currentConditions"]["conditions"]
    windgust = data["currentConditions"]["windgust"]
    windspeed = data["currentConditions"]["windspeed"]
    datetime = data["currentConditions"]["datetime"]
    humidity = data["currentConditions"]["humidity"]
    uvindex = data["currentConditions"]["uvindex"]

    # Parse other weather attributes similarly
    weather_data = WeatherData(
        temperature=temperature,
        precipitation=precipitation,
        precipitation_probability=precipitation_probability,
        cloudcover = cloudcover,
        conditions = conditions,
        windgust = windgust,
        windspeed = windspeed,
        datetime = datetime,
        humidity = humidity,
        uvindex = uvindex,
        # Set other attributes accordingly
    )
    return weather_data


def get_virtual_coach_response(user_query):
    # Tokenize the user query
    tokens = word_tokenize(user_query)

    # Perform part-of-speech tagging
    tagged_tokens = pos_tag(tokens)

    # Extract keywords from the tagged tokens
    keywords = [token[0] for token in tagged_tokens if token[1].startswith('NN')]

    # Match the keywords with the conversational flow dictionary
    for intent, data in conversational_flow['intents'].items():
        for question in data['questions']:
            # Tokenize and extract keywords from the question
            question_tokens = word_tokenize(question)
            question_keywords = [token for token in question_tokens if token in keywords]

            # Check if the question keywords match with user query keywords
            if len(question_keywords) == len(keywords):
                return random.choice(data['responses'])

    return "I'm sorry, but I don't have the information you're looking for."


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


@app.post("/recommendation")
def send_recommendation(user_preferences: UserPreferences, weather_data: WeatherData):
    # Initialize the recommendation engine
    recommendation_engine = ClothingRecommendation()

    # Process user preferences and weather data if necessary
    # ...

    # Generate clothing recommendations
    recommendation = recommendation_engine.generate_recommendation(weather_data, user_preferences)

    return {"recommendation": recommendation}


@app.post('/virtual_coach')
async def virtual_coach(request: Request):
    data = await request.json()
    user_query = data['query']
    response = get_virtual_coach_response(user_query)
    return JSONResponse({'response': response})
