import requests
from bs4 import BeautifulSoup
import lxml


BROWSER_USER_AGENT = ""         # @TODO
BROWSER_ACCEPT_LANGUAGE = ""    # @TODO


class AmazonInterface:

    def get_item(self, product_url: str) -> (str, str):

        headers = {
            "Accept-Language": BROWSER_ACCEPT_LANGUAGE,
            "User-Agent": BROWSER_USER_AGENT
        }

        response = requests.get(url=product_url, headers=headers)
        content = BeautifulSoup(response.text, "lxml")
        name = content.find(name="span", id="productTitle", class_="a-size-large product-title-word-break")
        price = content.find(name="span", class_="a-price a-text-price a-size-medium").span

        return name.getText().strip(), price.getText()
