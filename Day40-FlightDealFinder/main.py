"""
    Program written to find cheapest flight to specified destinations inside of a google sheet.

    Originally was made with the intention of sending a text message. Changed it to send an email instead due to the
    trial restriction of twilio.

    APIs used:
        Tequila - Kiwi.com
        Sheety
"""

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
#   @TODO: UPDATE CONSTANTS IN OTHER CLASS FILES OR PROGRAM WILL NOT FUNCTION AT ALL
"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

flight_search = FlightSearch()
i = 0
for city in sheet_data:
    if city["iataCode"] == '':
        data_manager.data_index_needs_updated[i] = True
        city["iataCode"] = flight_search.get_destination_code(city=city["city"])
    i += 1

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# @TODO UPDATE THESE TO THE PROPER VALUES
departure_iata = ""  #departure_iata is the code used to identify your city that you are flying from
currency = ""

# used to determine how far out a flight can be date-wise.
date_boundary = 6 * 30  # default is 6 months at 30 days per month

flights_found = flight_search.search_for_flights(sheet_data, departure_iata, date_boundary, currency)

notification_manager = NotificationManager()
flights = []
for i in range(len(flights_found)):
    """
        Put only the ones that meet criteria, into a list
    """
    if flights_found[i].price <= sheet_data[i]["lowestPrice"]:
        flights.append(flights_found[i])

notification_manager.send_email_alert(flights=flights, data_manager=data_manager)
