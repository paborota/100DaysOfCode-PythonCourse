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

    def find_flight(self, city, departure_iata, date_boundary, currency, num_of_stopovers):

        headers = {
            "apikey": FLIGHT_KEY
        }
        flight_params = {
            "fly_from": departure_iata,
            "fly_to": city["iataCode"],
            "date_from": (datetime.today().date() + timedelta(days=+1)).strftime("%d/%m/%Y"),
            "date_to": (datetime.today().date() + timedelta(days=+(1 + date_boundary))).strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": num_of_stopovers,
            "curr": currency,
            "locale": "en",
        }

        flight_search_endpoint = f"{FLIGHT_ENDPOINT}v2/search"
        response = requests.get(url=flight_search_endpoint, headers=headers, params=flight_params)
        return response.json()

    def search_for_flights(self, cities, departure_iata, date_boundary, currency):

        flights = []
        for city in cities:
            response_data = self.find_flight(city, departure_iata, date_boundary, currency, 0)
            if len(response_data["data"]) == 0:
                print("\nFirst check did not succeed, trying with 1 stop over...\n")
                response_data = self.find_flight(city, departure_iata, date_boundary, currency, 1)
                if len(response_data["data"]) == 0:
                    print(f"\nSecond check did not succeed, no flights found for {city['city']}")
                    continue

            flight = FlightData(response_data)
            print(flight)
            flights.append(flight)

        return flights

