import smtplib
from email.message import EmailMessage
import requests
import os
from dotenv import load_dotenv
from db import add_crypto, update_crypto, get_all, get_crypto



# config
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL') # could be same as EMAIL_ADDRESS

API_KEY = os.getenv('API_KEY')

PERCENT_THRESHOLD = 2.0


def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        connection.send_message(msg)

    print("Email sent.")


def get_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": API_KEY
    }
    response = requests.get(url, headers=headers)

    return response.json()[symbol]["usd"]


def update_all():
    db_cryptos = get_all()
    symbols = ",".join([crypto[1] for crypto in db_cryptos])
    tickers = [crypto[0] for crypto in db_cryptos]
    old_prices = [crypto[2] for crypto in db_cryptos]

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbols}&vs_currencies=usd"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": API_KEY
    }
    response = requests.get(url, headers=headers)

    for ticker in tickers:
        price = response.json()[get_crypto(ticker)[1]]["usd"]
        update_crypto(ticker, price)

        if price > old_prices[tickers.index(ticker)] * (1 + PERCENT_THRESHOLD / 100):
            send_email(f"{ticker} Alert", f"{ticker} has increased by more than {PERCENT_THRESHOLD}% in the last hour.")
        elif price < old_prices[tickers.index(ticker)] * (1 - PERCENT_THRESHOLD / 100):
            send_email(f"{ticker} Alert", f"{ticker} has decreased by more than {PERCENT_THRESHOLD}% in the last hour.")





if __name__ == "__main__":
    update_all()
    #print(get_all())
