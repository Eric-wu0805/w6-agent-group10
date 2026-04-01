import sys
import requests

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        desc = current['weatherDesc'][0]['value']
        print(f"{temp_c}°C，{desc}")
    except Exception as e:
        print(f"Error fetching weather: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_weather(sys.argv[1])
    else:
        print("Usage: python get_weather.py <city>")
