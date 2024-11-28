import requests

API_KEY = "FKcXxykJPpIn3WOSPYlZo9jMwpQXXB9o"  # Replace with your actual Tomorrow.io API Key

def get_weather_forecast(location="Bengaluru"):
    try:
        # Adjust URL to get forecast data
        url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={API_KEY}&timesteps=1h"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "timelines" in data and "hourly" in data["timelines"]:
            forecast_data = data["timelines"]["hourly"][:5]  # Get the next 5 hourly forecasts
            forecast_message = f"Weather forecast for {location}:\n"

            for forecast in forecast_data:
                time = forecast["time"]
                values = forecast["values"]
                forecast_message += (
                    f"\nTime: {time}\n"
                    f"Temperature: {values['temperature']}°C\n"
                    f"Humidity: {values['humidity']}%\n"
                    f"Wind Speed: {values['windSpeed']} m/s\n"
                    f"UV Index: {values['uvIndex']}\n"
                    f"Cloud Cover: {values['cloudCover']}%\n"
                    f"Precipitation Probability: {values['precipitationProbability']}%\n"
                    f"Visibility: {values['visibility']} km\n"
                )
            return forecast_message.strip()
        else:
            return "Weather forecast data is not available at the moment."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather forecast data: {e}"
