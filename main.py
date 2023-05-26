from fastapi import FastAPI
from pydantic import BaseModel

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

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the WhatToWear API!"}

