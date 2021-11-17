import requests
from bs4 import BeautifulSoup
import lxml

ZILLOW_URL = ""  # @TODO


class ZillowInterface:

    def __init__(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(ZILLOW_URL, headers=headers)
        self.soup = BeautifulSoup(response.text, "lxml")

    def get_listings(self) -> list[dict]:

        addresses = self.soup.select(".list-card-addr")
        prices = self.soup.select(".list-card-price")
        raw_links = self.soup.select(".list-card-top .list-card-link")
        print(len(raw_links))
        links = []
        for link in raw_links:
            try:
                if "https" not in link["href"]:
                    links.append("https://www.zillow.com"+link["href"])
                else:
                    links.append(link["href"])
            except KeyError:
                print("KeyError")
                pass

        listings = []
        for i in range(len(addresses)):
            listings.append(
                {
                    "Address": addresses[i].text,
                    "Price": prices[i].text,
                    "Link": links[i]
                }
            )

        for listing in listings:
            print(listing)
        return listings
