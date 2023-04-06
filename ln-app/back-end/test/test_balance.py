import requests

url = 'http://localhost:5000/balance'

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    balance = data['Balance']
    print(f"Total Balance: {balance}")
else:
    print(f"Error: {response.status_code}")