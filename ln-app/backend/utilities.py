import datetime
import os
import time
from coin import get_cash, reset_coin_value


import requests
import api
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

## test
#def get_total_eur():
#    total_money = get_total_money()
#    return total_money

#def reset():
#    reset_total_money()
#    return

# Initialize array to store Euros

def get_total_eur():
    total_money = get_cash()
    return total_money

def reset():
    reset_coin_value()
    return

def create_lnurl_withdraw_link(withdraw_amount):
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    api_key = os.getenv("API_KEY")  # Retrieve API key from environment variable
    LNURL = os.getenv("LNURL")
    balance = get_ln_wallet_balance(api_key, LNURL)  # Retrieve LN wallet balance using API key
    balance = balance / 1000
    
    # Check if balance is too low
    if balance is None:
        print("Balance is too low")
        return None

    # Check if withdrawal amount is greater than balance
    if withdraw_amount > balance:
        print("Withdrawal amount is greater than balance, cannot withdraw")
        return None

    # Construct URL for withdrawal link creation
    url = LNURL + "/withdraw/api/v1/links"

    # Define headers for the POST request
    headers = {
    "Content-type": "application/json",
    "X-Api-Key": api_key
    }

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
        "is_unique": False,
        "webhook_url": None
    }

    # Send POST request to LNURL API
    response = requests.post(url, json=body, headers=headers)

    # Check if response status code indicates successful creation of withdrawal link
    if response.status_code == 201:
        data = response.json()
        return data  # Extract "lnurl" field from response data and return it
    else:
        return None  # Return None if response status code is not 201


    
def delete_lnurl_withdraw_link(lnurlw):
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    api_key = os.getenv("API_KEY")
    invoice_key = os.getenv("invoice_key")
    API_URL = os.getenv("LNURL")

    withdraw_id = get_withdraw_id(lnurlw, API_URL, invoice_key)

    url = API_URL + '/withdraw/api/v1/links/' + withdraw_id['withdraw_id']
    headers = {'X-Api-Key': api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False

def get_withdraw_id(lnurl, API_URL, invoice_key):

    url = API_URL + '/withdraw/api/v1/links'
    headers = {'X-Api-Key': invoice_key}
  
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        links = response.json()

        for link in links:
            if link['lnurl'] == lnurl:
                return link['lnurl']
        return False
    else:
        print('HTTP request failed with status code:', response.status_code)
        return None
    


def get_ln_wallet_balance(api_key, LNURL):
    # Construct URL for retrieving LN wallet balance
    url = LNURL + "/api/v1/wallet"

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
    

def check_withdraw_link_status(lnurl):
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    invoice_key = os.getenv("invoice_key")  # Retrieve key from environment variable
    LNURL = os.getenv("LNURL")
    url = LNURL + '/withdraw/api/v1/links'
    headers = {'X-Api-Key': invoice_key}
  
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        links = response.json()

        for link in links:
            if link['lnurl'] == lnurl and link['used'] == 1:
                return True
        return False
    else:
        print('HTTP request failed with status code:', response.status_code)
        return None

def check_withdrawal_link():
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    api_key = os.getenv("API_KEY")  # Retrieve API key from environment variable
    LNURL = os.getenv("LNURL")

    url = LNURL + "/withdraw/api/v1/links"
    headers = {
        "X-Api-Key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        withdrawal_links = response.json()
        for link in withdrawal_links:
            if link["used"] == 0 and link["uses"] == 1:
                return {'lnurl': link["lnurl"], 'satoshi': link["max_withdrawable"]}
        return False
    else:
        print(f"Failed to fetch withdrawal links. Status code: {response.status_code}")
        return False

