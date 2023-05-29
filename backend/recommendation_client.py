import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("VISUAL_CROSSING_API_KEY")
location = "Gothenburg"
urlAPI = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=us&key={api_key}"

response = requests.get(urlAPI)
if response.status_code == 200:
    weather_data = response.json()
else:
    print("Failed to fetch weather data. Status code:", response.status_code)

current_conditions = weather_data['currentConditions']
temperature = current_conditions['temp']
precipitation_probability = current_conditions['precipprob']
precipitation = current_conditions['precip']
cloudcover = current_conditions['cloudcover']
conditions = current_conditions['conditions']
windgust = current_conditions['windgust']
windspeed = current_conditions['windspeed']
humidity = current_conditions['humidity']
uvindex = current_conditions['uvindex']

url = "http://localhost:8000/recommendation"
data = {
    "user_preferences": {
        "gender": "male",
        "comfort_level": "high"
    },
    "weather_data": {
        "temperature": temperature,
        "precipitation_probability": precipitation_probability,
        "precipitation": precipitation,
        "cloudcover": cloudcover,
        "conditions": conditions,
        "windgust": windgust,
        "windspeed": windspeed,
        "humidity": humidity,
        "uvindex": uvindex
    }
}
headers = {
    "Content-Type": "application/json"
}

print("City:", location)
print("Weather Data:")
print("Temperature:", temperature)
print("Precipitation Probability:", precipitation_probability)
print("Precipitation:", precipitation)
print("Cloud Cover:", cloudcover)
print("Conditions:", conditions)
print("Wind Gust:", windgust)
print("Wind Speed:", windspeed)
print("Humidity:", humidity)
print("UV Index:", uvindex)

response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    recommendation = response.json()
    print("Recommendation:", recommendation)
else:
    print("Failed to get a recommendation. Status code:", response.status_code)
