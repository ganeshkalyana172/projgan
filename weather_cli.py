try:
    import requests
except ImportError:
    print("Install requests first: python -m pip install requests")
    raise SystemExit(1)

CODES = {0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",45:"Fog",48:"Rime fog",51:"Light drizzle",53:"Drizzle",55:"Heavy drizzle",61:"Light rain",63:"Rain",65:"Heavy rain",71:"Light snow",73:"Snow",75:"Heavy snow",80:"Rain showers",81:"Rain showers",82:"Heavy rain showers",95:"Thunderstorm",96:"Thunderstorm with hail",99:"Thunderstorm with heavy hail"}
def main():
    city = input("Enter city name: ").strip()
    if not city: print("City name cannot be empty."); return
    try:
        r = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={"name":city,"count":1,"language":"en","format":"json"}, timeout=10); r.raise_for_status()
        places = r.json().get("results", [])
        if not places: print("City not found. Check spelling."); return
        place = places[0]
        r = requests.get("https://api.open-meteo.com/v1/forecast", params={"latitude":place["latitude"],"longitude":place["longitude"],"current":"temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m","timezone":"auto"}, timeout=10); r.raise_for_status()
        data = r.json(); now = data.get("current", {}); units = data.get("current_units", {})
        print("\n=== CURRENT WEATHER ===")
        print(f"Location: {place.get('name')}, {place.get('country','')}")
        print(f"Time: {now.get('time','N/A')}")
        print(f"Condition: {CODES.get(now.get('weather_code'), 'Unknown')}")
        print(f"Temperature: {now.get('temperature_2m','N/A')} {units.get('temperature_2m','°C')}")
        print(f"Feels like: {now.get('apparent_temperature','N/A')} {units.get('apparent_temperature','°C')}")
        print(f"Humidity: {now.get('relative_humidity_2m','N/A')} {units.get('relative_humidity_2m','%')}")
        print(f"Wind speed: {now.get('wind_speed_10m','N/A')} {units.get('wind_speed_10m','km/h')}")
    except requests.RequestException as e: print("Could not fetch weather. Check internet connection.\n", e)
if __name__ == "__main__": main()
