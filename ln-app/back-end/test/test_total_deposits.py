import requests


url = 'http://localhost:5000/total-deposits'

response = requests.get(url)

if response.status_code == 200:
    total_eur = response.json()['total_deposits']
    print(f"Total price in satoshi: {total_eur}")
else:
    print(f"Error: {response.status_code}")