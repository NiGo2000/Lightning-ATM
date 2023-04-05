import requests

url = 'http://localhost:5000/create-lnurl-withdraw-link'

response = requests.get(url)

if response.status_code == 200:
    lnurl_withdraw_link = response.text
    print(f"LNURL withdraw link: {lnurl_withdraw_link}")
else:
    print(f"Error: {response.status_code}")