import configparser
import json
from pathlib import Path
import urllib.parse
import urllib.request


# 1. Read credentials privately. They aren't saved to a file.
config_path = Path(__file__).resolve().parent / "config.ini"
config = configparser.ConfigParser(interpolation=None)
if not config.read(config_path, encoding="utf-8"):
    raise SystemExit(f"Missing configuration file: {config_path}")

client_id = config["xweather"]["client_id"]
client_secret = config["xweather"]["client_secret"]
location = config["xweather"]["location"].strip()



# 3. Request one forecast for each of the next 24 hourly periods.
params = urllib.parse.urlencode({
    "client_id": client_id,
    "client_secret": client_secret,
    "filter": "1hr",
    "limit": 24,
})

# 4. Use the forecast endpoint instead of the observation endpoint.
url = (
    "https://data.api.xweather.com/forecasts/"
    + urllib.parse.quote(location, safe=",")
    + "?"
    + params
)

try:
    # 5. Send the request and read the JSON response.
    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.load(response)

    if not data.get("success"):
        print("API error:", data.get("error"))
    else:
        forecast = data["response"][0]
        # Take the first 12 hourly forecast periods.
        next_12_hours = forecast["periods"][:12]

        # Keep temperatures that are available; missing values aren't zero.
        temperatures = [
            period["tempC"]
            for period in next_12_hours
            if period.get("tempC") is not None
        ]

        if len(temperatures) != 12:
            print("\nNot enough data for a complete 12-hour check.")
        else:
            minimum = min(temperatures)
            freezing = minimum < 0

            print(f"\nLowest forecast temperature: {minimum:.1f}°C")
            print("Freezing forecast:", "YES" if freezing else "NO")
        
        print("\nForecast interval:", forecast.get("interval"))
        print("Time | Predicted temperature (°C)")

        # 6. Print only the time and temperature for each period.
        for period in forecast["periods"]:
            print(period["dateTimeISO"], "|", period.get("tempC"))

except Exception:
    print("Request failed. Check your connection and API access.")