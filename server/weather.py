from typing import Any, Dict
import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
WEATHER_API_BASE = "http://api.weatherapi.com/v1"
API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("WEATHER_API_KEY environment variable is not set")

async def make_weather_request(endpoint: str, params: Dict[str, str]) -> Dict[str, Any] | None:
    """Make a request to the WeatherAPI with proper error handling."""
    params["key"] = API_KEY
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{WEATHER_API_BASE}/{endpoint}", params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making weather request: {str(e)}")
            return None

def format_weather(data: Dict[str, Any]) -> str:
    """Format weather data into a readable string."""
    current = data["current"]
    location = data["location"]
    return f"""
    Location: {location['name']}, {location['region']}, {location['country']}
    Temperature: {current['temp_c']}°C
    Condition: {current['condition']['text']}
    Humidity: {current['humidity']}%
    Wind Speed: {current['wind_kph']} km/h
    Last Updated: {current['last_updated']}
    """

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """Get current weather for a city in India.

    Args:
        city: Name of the city in India (e.g. Mumbai, Delhi, Bangalore)
    """
    params = {
        "q": f"{city},India",
        "aqi": "no"
    }
    data = await make_weather_request("current.json", params)

    if not data:
        return "Unable to fetch weather data. Please check the city name and try again."

    return format_weather(data)

@mcp.tool()
async def get_forecast(city: str, days: int = 3) -> str:
    """Get weather forecast for a city in India.

    Args:
        city: Name of the city in India (e.g. Mumbai, Delhi, Bangalore)
        days: Number of days for forecast (1-3)
    """
    if not 1 <= days <= 3:
        return "Forecast days must be between 1 and 3"

    params = {
        "q": f"{city},India",
        "days": str(days),
        "aqi": "no"
    }
    data = await make_weather_request("forecast.json", params)

    if not data:
        return "Unable to fetch forecast data. Please check the city name and try again."

    forecast = data["forecast"]["forecastday"]
    location = data["location"]
    
    result = [f"Weather Forecast for {location['name']}, {location['region']}, {location['country']}"]
    
    for day in forecast:
        date = day["date"]
        max_temp = day["day"]["maxtemp_c"]
        min_temp = day["day"]["mintemp_c"]
        condition = day["day"]["condition"]["text"]
        result.append(f"""
        Date: {date}
        Condition: {condition}
        Temperature: {min_temp}°C to {max_temp}°C
        """)
    
    return "\n".join(result)
