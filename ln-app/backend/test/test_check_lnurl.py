import requests

url = 'http://localhost:5000/check-withdrawal-link'


response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    if data is False:
        print(f"payment success: {data}")
    else:
        lnurl = data['lnurl']
        satoshi = data['satoshi']
        print(f"lnurl: {lnurl}")
        print(f"satoshi: {satoshi}")
else:
    print(f"Error: {response.status_code}")