# API from CoinGecko for Bitcoin price
def bitcoinApi(cg):
    data = cg.get_price(ids='bitcoin', vs_currencies='eur')
    btc_price = float(data["bitcoin"]["eur"])
    return btc_price

LNURL = "https://ln.pixeldev.eu:3007"



