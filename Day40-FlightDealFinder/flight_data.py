class FlightData:
    #This class is responsible for structuring the flight data.

    def __init__(self, flight):

        self.price = flight["data"][0]["conversion"]["GBP"]
        self.departure_airport_code = flight["data"][0]["flyFrom"]
        self.departure_city = flight["data"][0]["cityFrom"]
        self.arrival_airport_code = flight["data"][0]["flyTo"]
        self.arrival_city = flight["data"][0]["cityTo"]
        self.out_date = flight["data"][0]["route"][0]["local_departure"].split('T')[0]

        if len(flight["data"][0]["route"]) == 4:
            self.return_date = flight["data"][0]["route"][3]["local_departure"].split('T')[0]
            self.stop_overs = 1
            self.so_via_city = flight["data"][0]["route"][0]["cityTo"]
        else:
            self.return_date = flight["data"][0]["route"][1]["local_departure"].split('T')[0]
            self.stop_overs = 0
            self.so_via_city = ''

    def __str__(self):
        if self.stop_overs == 1:
            return "Flight:\n" \
                   f"\t{self.departure_city} -> {self.arrival_city}" \
                   f"\tFlight has {self.stop_overs} stop over, via {self.so_via_city}" \
                   f"\t\tPrice: " + u"\xA3" + f"{self.price}"
        else:
            return "Flight:\n" \
                  f"\t{self.departure_city} -> {self.arrival_city}\n" \
                  f"\t\tPrice: {self.price}"
