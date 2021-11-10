from flight_data import FlightData
import smtplib
from typing import List


# ------------------- SMTP CONSTANTS ------------------- #
#TODO: UPDATE THESE CONSTANTS AS NEEDED OTHERWISE WON'T WORK

EMAIL_SMTP = ""

EMAIL = ""
PASSWORD = ""


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def send_email_alert(self, flights: List[FlightData]):
        data = ''
        for flight in flights:
            # we know everything passed in is a discount, so just format for email
            data += "Flight details:\n" \
                    f"\tFrom: {flight.departure_city}\n" \
                    f"\tTo: {flight.arrival_city}\n" \
                    f"\tDeparture Date: {flight.out_date}\n" \
                    f"\tReturn Date: {flight.return_date}\n" \
                    f"\t\tPrice: {flight.price}\n\n"

        with smtplib.SMTP(EMAIL_SMTP) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=EMAIL,
                                msg="Subject:Flight Discounts Found!!\n\n"
                                    + data)
