import datetime
import json
import os
import qrcode
import time

import requests
import api
from PySide6.QtGui import QPixmap
from PIL import ImageQt
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv

from test_money import get_total_money, reset_total_money

# caching the Bitcoin price for 6 seconds
cache_timeout = 6
last_fetch_time = None
btc_price_cache = None

# get Bitcoin price and return it to app.py
def get_btc_price():
    cg = CoinGeckoAPI()
    global last_fetch_time, btc_price_cache
    if last_fetch_time is None or time.time() - last_fetch_time > cache_timeout:
        try:
            # storing the Bitcoin rate as a decimal number
            btc_price_cache = api.bitcoinApi(cg)
            last_fetch_time = time.time()
        except requests.exceptions.ConnectionError: 
            print("Error: No internet connection available.")
            btc_price_cache = None
    
    return btc_price_cache


# check if lnurl withdraw is accepted
def check_payment(self):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            return True
        time.sleep(0.1)

# conversion of the purchase in EUR to Bitcoin in Satoshis
def calculate_satoshi(eur_price):
    btc_price = get_btc_price()
    satoshi_price = int(eur_price * 1e8 / btc_price)
    return satoshi_price

# get invoice for lnurl withdraw
def generate_invoice(eur_price):
    invoice = "google.de"
    return invoice

# generate qr code with invoice
def generate_qr_code(invoice, qr_label):
    # creation of the QR code
    qr = qrcode.QRCode(version=None, box_size=2, border=4)
    qr.add_data(invoice)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # converting the PilImage to a QImage
    qimage = ImageQt.ImageQt(qr_image)
    # creating the QPixmap from the QImage
    qr_pixmap = QPixmap.fromImage(qimage)

    # display of the QR code in the GUI
    qr_label.setPixmap(qr_pixmap)

def get_total_eur():
    total_money = get_total_money()
    return total_money

def reset():
    reset_total_money()
    return

def create_lnurl_withdraw_link(withdraw_amount):
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("API_KEY")  # Retrieve API key from environment variable
    balance = get_ln_wallet_balance(api_key)  # Retrieve LN wallet balance using API key

    # Check if balance is too low
    if balance is None:
        print("Balance is too low")
        return None

    # Check if withdrawal amount is greater than balance
    if withdraw_amount > balance:
        print("Withdrawal amount is greater than balance, cannot withdraw")
        return None

    # Construct URL for withdrawal link creation
    url = api.LNURL + "/withdraw/api/v1/links"

    # Define headers for the POST request
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}

    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time as a string
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    # Construct request body with provided parameters
    body = {
        "title": "Withdraw at " + formatted_datetime,
        "min_withdrawable": 10,
        "max_withdrawable": withdraw_amount,
        "uses": 1,
        "wait_time": 1,
        "is_unique": True,
        "webhook_url": None
    }

    # Send POST request to LNURL API
    response = requests.post(url, json=body, headers=headers)

    # Check if response status code indicates successful creation of withdrawal link
    if response.status_code == 201:
        data = response.json()
        return data["lnurl"]  # Extract "lnurl" field from response data and return it
    else:
        return None  # Return None if response status code is not 201


    
def delete_lnurl_withdraw_link(the_hash, lnurl_id, invoice_key):
    # Construct URL for deleting the withdrawal link
    url = f"{api.LNURL}/withdraw/api/v1/links/{the_hash}/{lnurl_id}"

    # Define headers for the DELETE request
    headers = {"X-Api-Key": invoice_key}

    # Send DELETE request to LNURL API
    response = requests.delete(url, headers=headers)

    # Check if response status code indicates successful deletion (status code 200)
    if response.status_code == 200:
        return True  # Return True if deletion is successful
    else:
        return False  # Return False if deletion is not successful


def get_ln_wallet_balance(api_key):
    # Construct URL for retrieving LN wallet balance
    url = api.LNURL + "/api/v1/wallet"

    # Define headers for the GET request
    headers = {"X-Api-Key": api_key}

    # Send GET request to LNURL API
    response = requests.get(url, headers=headers)

    # Check if response status code indicates successful retrieval (status code 200)
    if response.status_code == 200:
        data = response.json()
        return data["balance"]  # Return the balance from the response data
    else:
        return None  # Return None if retrieval is not successful
