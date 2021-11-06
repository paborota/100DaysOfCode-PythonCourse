import requests
from datetime import datetime as dt
from math import sqrt
import smtplib
import time


# ---------------------------- CONSTANTS ---------------------------------#
MY_LAT = 0 # INSERT LATITUDE SETTING
MY_LONG = 0 # INSERT LONGITUDE SETTING

LOCAL_UTC_OFFSET = 0 # INSERT TIMEZONE DIFFERENCE FROM UTC

MY_EMAIL = "" # INSERT EMAIL HERE
MY_PASSWORD = "" # INSERT PASSWORD HERE


# ---------------------------- FUNCTIONALITY ---------------------------------#
def check_in_range():
    global MY_LAT
    global MY_LONG

    # Call to the API and receive data appropriately
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    # Grab latitude and longitude from the data received
    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])

    # Check distance between the two points, the CONSTANT lat and long VS the ones received
    # consider latitude X and longitude Y for points on a 2D plane
    # return True if within distance, False if not
    distance = abs(sqrt(pow(latitude - MY_LAT, 2) + pow(longitude - MY_LONG, 2)))
    print(distance)
    if distance <= 5:
        return True
    return False


def check_is_nighttime():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    # API call and receive
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()

    # Pull sunrise and sunset information
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]
    rise_hour = int(sunrise.split('T')[1].split(':')[0])
    set_hour = int(sunset.split('T')[1].split(':')[0])

    # Add CONSTANT local offset and then fix if time went over the outer limits 0 - 24
    time_now_hour = dt.now().hour + LOCAL_UTC_OFFSET
    if time_now_hour > 24:
        time_now_hour -= 24
    elif time_now_hour < 0:
        time_now_hour += 24

    # Check sunrise and sunset info against current local time
    if time_now_hour < rise_hour or time_now_hour > set_hour:
        return True
    return False


if __name__ == "__main__":
    # Design with the idea that the code will constantly be running
    while True:

        time.sleep(60) # offset each check by 60 seconds

        # check both if it is nighttime and if the ISS is in range.
        # if so, email myself to "Look Up"
        if check_is_nighttime() and check_in_range():

            with smtplib.SMTP("smtp.google.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg="Subject:Look Up ☝️\n\n"
                        + "The ISS is overhead!"
                )
