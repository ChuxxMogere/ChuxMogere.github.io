import requests

API_KEY = "c178428bc5e6759e4bdc255c718013f6"


def get_weather_data(city_name):
    api_key = "c178428bc5e6759e4bdc255c718013f6"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Could not fetch weather data for '{city_name}'. Please try again."}


def get_weather_forecast(city_name):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if not geo_data:
        return {"error": "City not found"}

    lat, lon = geo_data[0]['lat'], geo_data[0]['lon']


    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(forecast_url)
    return response.json()

