import console.utilities as utilities

# conversion of the purchase in EUR to Bitcoin in Satoshis
def calculate_satoshi(eur_price, btc_price):
    satoshi_price = int(eur_price * 1e8 / btc_price)
    return satoshi_price

while True:
    # Start
    print("\nWillkommen! Bitte gib einen Betrag in EUR ein (oder 'q' zum Beenden, 'e' zum Abbrechen):")
    total_eur = 0

    # loop for the ATM
    while True:

        # storing the Bitcoin rate as a decimal number
        btc_price = utilities.get_btc_price()

        eur_input = input("> ")

        # when button was pressed create lnurl qr code and wait for confirmation of payment
        if eur_input.lower() == 'q':
            utilities.qrcode_invoice()
            if utilities.check_payment():
                print("Es wurden " + str(total_eur) + " EUR in " + str(calculate_satoshi(total_eur, btc_price)) + " Satoshis versendet")
                break
            else:
                print("Zahlung nicht bestätigt.")
            break
        # when this button is pressed, the money is returned again 
        elif eur_input.lower() == 'e':
            print("Wechsel wurde abgebrochen. Es werden " + str(total_eur) + " EUR ausgegeben.")
            break

        try:
            eur_price = float(eur_input)
            satoshi_price = calculate_satoshi(eur_price, btc_price)
            total_eur += eur_price
            print(str(eur_price) + " EUR in Bitcoin: " + str(satoshi_price) + " Satoshis")
            print("Gesamt in EUR: " + str(total_eur))
            print("Gesamt in Satoshi: " + str(calculate_satoshi(total_eur, btc_price)))
        except ValueError:
            print("Ungültige Eingabe. Bitte gib eine Zahl ein oder 'q' zum Beenden.")


