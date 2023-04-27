import requests

url = 'http://localhost:5000/check-payment'


response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    payment = data['payment']
    print(f"payment success: {payment}")
else:
    print(f"Error: {response.status_code}")