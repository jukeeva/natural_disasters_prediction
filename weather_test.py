import getpass
import json
import urllib.parse
import urllib.request

# 1. Read credentials privately. They aren't saved to a file.
client_id = getpass.getpass("Client ID: ")
client_secret = getpass.getpass("Client secret: ")

# 2. Choose the location to forecast.
location = input("Location as latitude,longitude: ").strip()

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
        print("\nForecast interval:", forecast.get("interval"))
        print("Time | Predicted temperature (°C)")

        # 6. Print only the time and temperature for each period.
        for period in forecast["periods"]:
            print(period["dateTimeISO"], "|", period.get("tempC"))

except Exception:
    print("Request failed. Check your connection and API access.")