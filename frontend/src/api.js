import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Replace with your backend server URL

export const fetchWeather = async (location) => {
  try {
    const response = await axios.get(`${API_URL}/weather?location=${location}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching weather:', error);
    throw error;
  }
};

export const sendUserPreferences = async (userPreferences, weatherData) => {
  try {
    const response = await axios.post(`${API_URL}/recommend`, { userPreferences, weatherData });
    return response.data;
  } catch (error) {
    console.error('Error sending user preferences:', error);
    throw error;
  }
};
