import requests
import json
from datetime import datetime, timezone

API_KEY = "FKcXxykJPpIn3WOSPYlZo9jMwpQXXB9o"  # Replace with your actual Tomorrow.io API Key

def get_weather_forecast(location="Bengaluru"):
    try:
        # Adjust URL to get forecast data
        url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={API_KEY}&timesteps=1h"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Print the JSON data to inspect its structure
        print(json.dumps(data, indent=2))  # Inspect the entire JSON response

        if "timelines" in data and "hourly" in data["timelines"]:
            forecast_data = data["timelines"]["hourly"][:5]  # Get the next 5 hourly forecasts
            forecast_message = f"Weather forecast for {location}:\n"
            rain_alert = None

            for i, forecast in enumerate(forecast_data):
                time = forecast["time"]
                values = forecast["values"]

                # Print to confirm access to the humidity value
                print(f"Hour {i+1} forecast: {values}")

                humidity = values.get("humidity")
                
                # Check for high humidity and set rain alert
                if humidity and humidity > 95 and rain_alert is None:
                    # Parse forecast time and make it UTC-aware
                    forecast_time = datetime.fromisoformat(time.replace("Z", "+00:00"))
                    # Make current time UTC-aware
                    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
                    hours_until_rain = int((forecast_time - current_time).total_seconds() // 3600)
                    rain_alert = f"Rain is likely to come in the next {hours_until_rain} hours."
                
                # Add forecast details to message
                forecast_message += (
                    f"\nTime: {time}\n"
                    f"Temperature: {values['temperature']}°C\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind Speed: {values['windSpeed']} m/s\n"
                    f"UV Index: {values['uvIndex']}\n"
                    f"Cloud Cover: {values['cloudCover']}%\n"
                    f"Precipitation Probability: {values['precipitationProbability']}%\n"
                    f"Visibility: {values['visibility']} km\n"
                )

            # Append rain alert message if set
            if rain_alert:
                forecast_message += f"\n\n{rain_alert}"
                
            return forecast_message.strip()
        else:
            return "Weather forecast data is not available at the moment."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather forecast data: {e}"

# Call the function for testing
print(get_weather_forecast("Mysore"))
