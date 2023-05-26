import React, { useState } from 'react';
import { fetchWeather, sendUserPreferences } from './api';

const WeatherForm = () => {
  const [location, setLocation] = useState('');
  const [weatherData, setWeatherData] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await fetchWeather(location);
      setWeatherData(data);
    } catch (error) {
      console.error('Error fetching weather:', error);
    }
  };

  const handleRecommendation = async () => {
    // Implement logic to gather user preferences (gender, comfort level, etc.)
    const userPreferences = { gender: 'male', comfort_level: 'moderate' };

    try {
      const data = await sendUserPreferences(userPreferences, weatherData);
      // Process the recommendation data
    } catch (error) {
      console.error('Error sending user preferences:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Enter location"
        />
        <button type="submit">Get Weather</button>
      </form>
      {weatherData && (
        <div>
          {/* Display the weather data */}
        </div>
      )}
      <button onClick={handleRecommendation}>Get Recommendation</button>
    </div>
  );
};

export default WeatherForm;
