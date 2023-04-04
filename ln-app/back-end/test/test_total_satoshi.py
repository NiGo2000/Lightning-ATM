import requests
import time

url = 'http://localhost:5000/total-price'

while True:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        total_satoshi = data['total_price_satoshi']
        total_eur = data['total_price_eur']
        print(f"Total price in satoshi: {total_satoshi}")
        print(f"Total price in euro: {total_eur}")
    else:
        print(f"Error: {response.status_code}")
    time.sleep(0.5)
