import requests
from datetime import datetime
from bs4 import BeautifulSoup


BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"
EARLIEST_DATE = datetime(1958, 8, 4)


class BillboardInterface:

    def __init__(self):
        self.billboard_date = self.get_user_entered_date()
        response = requests.get(f"{BILLBOARD_URL}{self.billboard_date}")
        self.soup = BeautifulSoup(response.text, "lxml")
        self.tracks = self.get_tracks()

    def get_tracks(self) -> list[dict]:

        song_tags = self.soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
        artist_tags = self.soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")

        tracks = []
        for i in range(len(song_tags)):
            tracks.append({"title": song_tags[i].getText(), "artist": artist_tags[i].getText()})

        return tracks

    def get_user_entered_date(self) -> str:
        input_accepted = False
        while not input_accepted:
            try:
                date = input("Enter in the date you'd like to grab music from (yyyy-mm-dd):\n")
                dt_input = datetime.strptime(date, "%Y-%m-%d")
                self.check_if_date_is_valid(dt_input)
            except ValueError:
                print("Incorrect input.")
            else:
                input_accepted = True
        return dt_input.date()

    def check_if_date_is_valid(self, dt_input) -> bool:
        if dt_input > datetime.now():
            print("You cannot enter a date that hasn't happened yet.")
            return False
        elif dt_input < EARLIEST_DATE:
            print("Earliest date accessible is 1958-08-04. Defaulting to that.")
        return True
