import requests

# ---------------------- SHEETY CONSTANTS -------------------- #
# TODO: UPDATE THESE CONSTANTS AS NEEDED OR WON'T WORK

SHEETY_URL = "https://api.sheety.co/"
SHEETY_USERNAME = ""
SHEETY_PROJECT = ""
SHEETY_SHEET = ""
SHEETY_ENDPOINT = f"{SHEETY_URL}/{SHEETY_USERNAME}/{SHEETY_PROJECT}/{SHEETY_SHEET}"

SHEETY_KEY = ""

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.destination_data = {}

        # List used to check if a value has been updated and needs to be
        # updated on the google sheet
        self.data_index_needs_updated = []

    def get_destination_data(self):
        """
            Grab all data from the google sheet and return it
        """
        headers = {
            "Authorization": f"Bearer {SHEETY_KEY}"
        }

        response = requests.get(url=SHEETY_ENDPOINT, headers=headers)
        data = response.json()
        self.destination_data = data["prices"]
        self.data_index_needs_updated = [False for _ in range(len(self.destination_data))]
        return self.destination_data

    def update_destination_codes(self):
        i = 0
        for city in self.destination_data:
            # Only update if there is a need to update.
            # Because SHEETY really got that low 200 request limit sheesh.
            if self.data_index_needs_updated[i]:
                new_data = {
                    "price": {
                        "iataCode": city["iataCode"]
                    }
                }
                headers = {
                    "Authorization": f"Bearer {SHEETY_KEY}"
                }

                edit_endpoint = f"{SHEETY_ENDPOINT}/{city['id']}"

                response = requests.put(url=edit_endpoint, json=new_data, headers=headers)
                response.raise_for_status()
            i += 1
