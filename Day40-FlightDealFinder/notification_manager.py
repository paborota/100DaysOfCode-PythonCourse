from flight_data import FlightData
from data_manager import DataManager
import smtplib
from typing import List


# ------------------- SMTP CONSTANTS ------------------- #
#TODO: UPDATE THESE CONSTANTS AS NEEDED OTHERWISE WON'T WORK

EMAIL_SMTP = ""
EMAIL = ""
PASSWORD = ""

# DOES NOT WORK PROPERLY LEAVE COMMENTED
# GOOGLE_LINK_BASE = "https://www.google.co.uk/flights?hl=en#"


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def send_email_alert(self, flights: List[FlightData], data_manager: DataManager):

        data = ''
        for flight in flights:
            # we know everything passed in is a discount, so just format for email
            data += f"{flight}\n"
                    # "Book your flight now with this link:\n" \
                    # f"{GOOGLE_LINK_BASE}" \
                    # f"flt={flight.departure_airport_code}.{flight.arrival_airport_code}.{flight.out_date}" \
                    # f"*{flight.arrival_airport_code}.{flight.departure_airport_code}.{flight.return_date}\n\n"

        clients = data_manager.get_user_data()
        for client in clients:
            with smtplib.SMTP(EMAIL_SMTP) as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=EMAIL,
                                    to_addrs=client["email"],
                                    msg="Subject:Flight Discounts Found!!\n\n"
                                        f"Hello, {client['firstName']}!\n"
                                        f"We found you some great deals on flights!\n\n"
                                        + data)
