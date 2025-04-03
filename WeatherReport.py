import requests
from Speak_func import speak
from GPS_Current_Location_giver import get_location
API_KEY = "9cf55da3440210f608c42be12ecc4992"  # Replace with your actual API key
my_current_location = []
if get_location() != None:
    my_current_location.clear()
    my_current_location.insert(0,get_location())
else:
    my_current_location.insert(0,get_location())


def get_weather():
    """Fetch the weather report for a given city"""
    city=my_current_location[0]['city']
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(URL)
    data = response.json()

    if response.status_code == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        result = f"The current weather in {city} is {weather} with a temperature of {temp}°C. but it feels like {feels_like}°C."
        speak(result)  # Speak the weather report
        return result
    else:
        error_message = f"Could not fetch weather data: {data.get('message', 'Unknown error')}"
        speak(error_message)
        return error_message
