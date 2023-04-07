import requests

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

url = "http://ln.pixeldev.eu:3007/api/v1/wallet"
headers = {"X-Api-Key": api_key}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    balance = data["balance"]
    print(f"Total Balance: {balance}")
else:
    print(f"Error: {response.status_code}")