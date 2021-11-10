import requests
from flight_data import FlightData
from datetime import datetime, timedelta

# ----------------------- KIWI CONSTANTS ----------------------- #
# TODO: UPDATE CONSTANTS OR WON'T WORK

FLIGHT_ENDPOINT = "https://tequila-api.kiwi.com/"
FLIGHT_KEY = ""


class FlightSearch:

    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city: str):
        params = {
            "term": city,
            "location_types": "city"
        }
        headers = {
            "apikey": FLIGHT_KEY
        }

        location_endpoint = f"{FLIGHT_ENDPOINT}locations/query"
        response = requests.get(url=location_endpoint, headers=headers, params=params)
        response.raise_for_status()

        code = response.json()["locations"][0]["code"]
        return code

    def find_flight(self, cities, depature_iata, date_boundary, currency):
        headers = {
            "apikey": FLIGHT_KEY
        }

        flights = []
        for city in cities:
            flight_params = {
                "fly_from": depature_iata,
                "fly_to": city["iataCode"],
                "date_from": (datetime.today().date() + timedelta(days=+1)).strftime("%d/%m/%Y"),
                "date_to": (datetime.today().date() + timedelta(days=+(1 + date_boundary))).strftime("%d/%m/%Y"),
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "one_for_city": 1,
                "max_stopovers": 0,
                "curr": currency,
                "locale": "en",
            }

            flight_search_endpoint = f"{FLIGHT_ENDPOINT}v2/search"
            response = requests.get(url=flight_search_endpoint, headers=headers, params=flight_params)
            data = response.json()["data"]
            if len(data) != 0:
                flight = FlightData(
                    price=data[0]["price"],
                    departure_airport_code=data[0]["cityCodeFrom"],
                    departure_city=data[0]["cityFrom"],
                    arrival_airport_code=data[0]["cityCodeTo"],
                    arrival_city=data[0]["cityTo"],
                    out_date=data[0]["route"][0]["local_departure"].split('T')[0],
                    return_date=data[0]["route"][1]["local_departure"].split('T')[0]
                )
                flights.append(flight)

        return flights

