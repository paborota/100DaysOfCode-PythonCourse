"""
    Program designed to reach out, using the Alpha Vantage API, and grab the stock prices of yesterday and the day before.
    Compare those values, and if the difference is greater than 5%, alert the user through a SMS message using Twilio.
    It also grabs the most recent article, using NewsAPI, that talks about the company.
"""

import requests
import os
from datetime import datetime as dt
from twilio.rest import Client


# ------------------------ CONSTANTS ------------------------- #
# ------------------ AlphaVantage CONSTANTS ------------------ #
STOCK_API = "https://www.alphavantage.co/query"
FUNCTION = "TIME_SERIES_DAILY"
STOCK = "TSLA"
OUTPUT_SIZE = "compact"
AlphaVantage_API_KEY = os.environ.get("AlphaVantage_API_KEY")

# ------------------ NewsAPI CONSTANTS ------------------ #
NEWS_API = "https://newsapi.org/v2/everything"
COMPANY_NAME = "Tesla Inc"
LANGUAGE = "en"
NEWS_API_KEY = os.environ.get("NewsAPI_API_KEY")

# ------------------ TWILIO CONSTANTS ------------------ #
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")

USER_PHONE = os.environ.get("USER_PHONE")
# ------------------------------------------------------ #
# ------------------------------------------------------ #


if __name__ == "__main__":

    stock_parameters = {
        "function": FUNCTION,
        "symbol": STOCK,
        "outputsize": OUTPUT_SIZE,
        "apikey": AlphaVantage_API_KEY
    }

    response = requests.get(STOCK_API, params=stock_parameters)
    print(response)
    response.raise_for_status()
    stock_data = response.json()["Time Series (Daily)"]
    stock_data_as_list = list(stock_data)[:2]

    print(stock_data_as_list)

    yesterday_key = stock_data_as_list[0]
    day_before_key = stock_data_as_list[1]

    yesterdays_close = float(stock_data[yesterday_key]["4. close"])
    day_before_close = float(stock_data[day_before_key]["4. close"])

    difference_percentage = ((yesterdays_close - day_before_close) / day_before_close) * 100
    if abs(difference_percentage) >= 0.001:

        news_parameters = {
            "qInTitle": COMPANY_NAME,
            "sortBy": "publishedAt",
            "language": LANGUAGE,
            "apiKey": NEWS_API_KEY
        }

        news_response = requests.get(NEWS_API, params=news_parameters)
        news_response.raise_for_status()
        first_three_articles = news_response.json()["articles"][:3]

        formatted_article_list = [f"Headline: {article['title']}\nBrief: {article['description']}" for article in first_three_articles]

        change_indicator = '🔻'
        if difference_percentage > 0:
            change_indicator = '🔺'

        message_body = f"{STOCK}: {change_indicator}{round(abs(difference_percentage), 2)}%\n\n" \
                       f"Headline: {first_three_articles[0]['title']}\n\n" \
                       f"Brief: {first_three_articles[0]['content']}"

        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
                body=message_body,
                from_=TWILIO_PHONE,
                to=USER_PHONE
            )
        print(message.status)
