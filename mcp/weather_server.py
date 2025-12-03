from mcp.server import Server
import requests
import os

# Note: This is a conceptual implementation based on the book's example.
# You would need a real 'mcp' library and an OpenWeatherMap API key.

server = Server("OpenWeatherMap MCP Server")
API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")

@server.tool()
def current_weather(location: str) -> dict:
    """Get current weather for any location
    Args:
        location: City name or coordinates
    Returns:
        Dictionary with temperature, condition, humidity, wind_speed
    """
    # Call OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": API_KEY, "units": "metric"}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["main"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def weather_forecast(location: str, days: int = 5) -> list:
    """Get weather forecast for upcoming days"""
    # Implementation placeholder
    return [{"day": i, "forecast": "Sunny"} for i in range(days)]

if __name__ == "__main__":
    print("Starting MCP Server...")
    # In a real scenario, this would block and listen for connections
    server.run()
