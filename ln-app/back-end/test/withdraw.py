import requests
from dotenv import load_dotenv
import os

# Die .env-Datei laden
load_dotenv()

# Den API-Schlüssel aus der Umgebungsvariable abrufen
api_key = os.getenv("API_KEY")

title = "My Withdraw Link"
withdraw_amount = 20
uses = 1
wait_time = 1
is_unique = True
webhook_url = None

url = "http://ln.pixeldev.eu:3007/withdraw/api/v1/links"
headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
body = {
    "title": title,
    "min_withdrawable": 10,
    "max_withdrawable": withdraw_amount,
    "uses": uses,
    "wait_time": wait_time,
    "is_unique": is_unique
}

if webhook_url is not None:
    body["webhook_url"] = webhook_url

response = requests.post(url, json=body, headers=headers)

if response.status_code == 201:
    data = response.json()
    print(data["lnurl"])
elif response.status_code == 400:
    print("Bad Request. Please check your request parameters.")
elif response.status_code == 401:
    print("Unauthorized. Please check your API key.")
elif response.status_code == 403:
    print("Forbidden. You don't have permission to access this resource.")
elif response.status_code == 500:
    print("Internal Server Error. Please try again later.")
else:
    print("Error occurred with status code:", response.status_code)