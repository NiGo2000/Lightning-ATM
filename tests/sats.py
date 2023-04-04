import requests

# API from CoinGecko for Bitcoin price
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur"

# Retrieving data from the API
response = requests.get(url)
data = response.json()

# Storing the Bitcoin rate as a decimal number
btc_price = float(data["bitcoin"]["eur"])


eur_price = float(input("Gib den Kaufpreis in EUR ein: "))

# Conversion of the purchase in EUR to Bitcoin in Satoshis
satoshi_price = int(eur_price * 100000000 / btc_price)

print("Bitcoin: " + str(btc_price) + " EUR")
print(str(eur_price) + " EUR in Bitcoin: " + str(satoshi_price) + " Satoshis")
