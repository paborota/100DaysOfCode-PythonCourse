"""
    Workout tracker using google sheets as the log.
    Takes advantage of:
        Nutritionix API
        Sheety API

    This file was uploaded and altered to work on replit.com
"""

from datetime import datetime as dt, timezone, timedelta
import requests
import os

# --------------------------------------------------------------- #
# -------------------- NUTRITIONIX CONSTANTS -------------------- #
NUTRITIONIX_ID = "5dc804ab"
NUTRITIONIX_KEY = os.environ["NUTRITIONIX_KEY"]
NUTRITIONIX_USER_ID = "0"

GENDER = "male"
WEIGHT_KG = "81.6"
HEIGHT_CM = "177.7"


# ---------------------------------------------------------- #
# -------------------- SHEETY CONSTANTS -------------------- #
SHEETY_USERNAME = "8ecf5257034ec52dd5efcd9e9f3f8d42"
SHEETY_PROJECT_NAME = "workoutTracking"
SHEETY_SHEET_NAME = "workouts"
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]


# -------------------------------------------------------------- #
# -------------------- NUTRITIONIX API CALL -------------------- #
headers = {
    "x-app-id": NUTRITIONIX_ID,
    "x-app-key": NUTRITIONIX_KEY,
    "x-remote-user-id": NUTRITIONIX_USER_ID
}

data = {
    "query": input("Enter what you did: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM
}

nutritionix_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

response = requests.post(url=nutritionix_exercise_endpoint, json=data, headers=headers)
response.raise_for_status()
workout_data = response.json()


# --------------------------------------------------------- #
# -------------------- SHEETY API CALL -------------------- #
sheety_endpoint = f"https://api.sheety.co/{SHEETY_USERNAME}/{SHEETY_PROJECT_NAME}/{SHEETY_SHEET_NAME}"

headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

# convert utc data into cdt (change per needed)
localized_time = dt.now(timezone(timedelta(hours=-6)))

for exercise in workout_data["exercises"]:
    """
        For every exercise that was inputted, we must create a seperate post to the sheet.
    """
    input_data = {
        "workout": {
            "date": localized_time.date().strftime("%d/%m/%Y"),
            "time": localized_time.time().strftime("%H:%M:%S"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    response = requests.post(url=sheety_endpoint, json=input_data, headers=headers)
    response.raise_for_status()
