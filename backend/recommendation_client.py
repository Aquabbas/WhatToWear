import requests

url = "http://localhost:8000/recommendation"
data = {
    "user_preferences": {
        "gender": "male",
        "comfort_level": "high"
    },
    "weather_data": {
        "temperature": 25.5,
        "precipitation": 0.0,
        "sky_conditions": "clear",
        "wind_conditions": "calm",
        "time_of_day": "morning",
        "humidity_level": 0.6,
        "uv_levels": 7.2
    }
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    recommendation = response.json()
    print("Recommendation:", recommendation)
else:
    print("Failed to get a recommendation. Status code:", response.status_code)
