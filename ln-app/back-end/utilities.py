import qrcode
import time

import requests
import api
from PySide6.QtGui import QPixmap
from PIL import ImageQt
from pycoingecko import CoinGeckoAPI

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


from test_money import get_total_money, reset_total_money

def get_total_eur():
    total_money = get_total_money()
    return total_money

def reset():
    reset_total_money()
    return
