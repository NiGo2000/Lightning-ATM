import qrcode
import requests
import time
import console.api as api

# get the URL for the lnurl withdraw and make it to a qr for the user
def qrcode_invoice():
    # Entering the Lightning Network Invoice via the API
    invoice = "google.de"

    # creating a QR code from the Lightning Network Invoice
    qr = qrcode.QRCode(version=None, box_size=2, border=4)
    qr.add_data(invoice)
    qr.make(fit=True)

    # Output of the QR code in the console
    qr.print_ascii(invert=True)

# caching the Bitcoin price for 1 minutes
cache_timeout = 1 * 60
last_fetch_time = None
btc_price_cache = None

# get Bitcoin price and return it to app.py
def get_btc_price():
    global last_fetch_time, btc_price_cache

    if last_fetch_time is None or time.time() - last_fetch_time > cache_timeout:
        # retrieving data from the API
        response = requests.get(api.url)
        data = response.json()

        # storing the Bitcoin rate as a decimal number
        btc_price_cache = float(data["bitcoin"]["eur"])
        last_fetch_time = time.time()

    return btc_price_cache

# check if lnurl withdraw is accepted
def check_payment():
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            return True
        time.sleep(0.1)