"""
    Program designed to reach out to OpenWeatherMap.org
    and then send a SMS alerting if it's going to rain
    at the designated city
"""

import os
import requests
from twilio.rest import Client

# ----------------------- OPEN WEATHER MAP CONSTANTS ----------------------- #
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.environ.get("OWM_API_KEY")

MY_LAT = "42.871059"
MY_LONG = "-97.390541"

EXCLUDE = "current,minutely,daily"

# ----------------------- TWILIO CONSTANTS ----------------------- #
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
USER_PHONE = os.environ.get("USER_PHONE")


weather_parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": EXCLUDE,
    "appid": API_KEY
}

response = requests.get(OWM_ENDPOINT, params=weather_parameters)
response.raise_for_status()
# print(response.status_code)

weather_data = response.json()

# Checking all conditions in the next 12 hours in the weather data
# and checking if it's in the correct weather condition code range - IE: raining/snowing
weather_slice = weather_data["hourly"][:12]

will_rain = False
for hourly_data in weather_slice:
    # there may be more than one condition in each hour
    for condition in hourly_data["weather"]:
        if condition["id"] < 700:
            will_rain = True

if will_rain:
    # it's going to rain, send the alert
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
            body="It's going to rain today, make sure to bring an ☂️",
            from_=TWILIO_PHONE,
            to=USER_PHONE
        )
    print(message.status)
