import RPi.GPIO as GPIO

coin_pin = 6
total_eur = 0

def get_pulse_count():
    pulse_count = 0
    while True:
        if GPIO.input(coin_pin) == GPIO.LOW:
            pulse_count += 1
            while GPIO.input(coin_pin) == GPIO.LOW:
                pass  # Wait for coin to be removed from coin slot
            return pulse_count

def recognize_coin(pulse_count):
    if pulse_count == 2:
        return 0.05
    elif pulse_count == 3:
        return 0.10
    elif pulse_count == 4:
        return 0.20
    elif pulse_count == 5:
        return 0.50
    elif pulse_count == 6:
        return 1.00
    elif pulse_count == 7:
        return 2.00
    else:
        return 0

def add_coin():
    global total_eur
    pulse_count = get_pulse_count()
    coin_value = recognize_coin(pulse_count)
    total_eur += coin_value
    return total_eur

if __name__ == "__main__":
    while True:
        pulse_count = get_pulse_count()
        coin_value = recognize_coin(pulse_count)
        if coin_value != 0:
            print("Eine Münze im Wert von {} Eurocent wurde eingeworfen".format(int(coin_value*100)))

