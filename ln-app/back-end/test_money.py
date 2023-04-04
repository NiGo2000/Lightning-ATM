total_money_file = 'total_money.txt'
total_money = 0

def add_coin(coin_value):
    global total_money
    with open(total_money_file, 'r') as f:
        total_money = int(f.read())
    total_money += coin_value
    with open(total_money_file, 'w') as f:
        f.write(str(total_money))


def get_total_money():
    global total_money
    try:
        with open(total_money_file, 'r') as f:
            total_money = int(f.read())
    except FileNotFoundError:
        total_money = 0
    return total_money

def reset_total_money():
    global total_money
    total_money = 0
    with open(total_money_file, 'w') as f:
        f.write(str(total_money))

def reset():
    reset_total_money()
    print("Total money has been reset to 0.")

if __name__ == "__main__":

    while True:
        coin_input = input("Bitte Münzwert eingeben (1/2) oder 'exit' zum Beenden: ")

        if coin_input == "exit":
            break
        
        if coin_input == "refund":
            reset()

        try:
            coin_value = int(coin_input)
        except ValueError:
            continue

        if coin_value not in [1, 2]:
            print("Ungültige Eingabe. Bitte nur '1', '2' oder 'exit' eingeben.")
            continue

        add_coin(coin_value)
        total_money_1 = get_total_money()

        print(f"Gesamt-Einzahlungsbetrag: {total_money_1:.2f} €")
