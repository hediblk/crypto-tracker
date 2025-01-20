import smtplib
from email.message import EmailMessage
import requests
import time
import os
from dotenv import load_dotenv


# email config
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL') # could be same as EMAIL_ADDRESS

# crypo api config
API_KEY = os.getenv('API_KEY')

COIN_IDS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "ripple": "XRP",
} 


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



def get_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": API_KEY
    }

    response = requests.get(url, headers=headers)

    return response.json()[symbol]["usd"]


if __name__ == "__main__":
    for key in COIN_IDS:
        print(get_price(key))
        time.sleep(5)
