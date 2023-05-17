import RPi.GPIO as GPIO

coin_pin = 6

def get_pulse_count():
    pulse_count = 0
    while True:
        if GPIO.input(coin_pin) == GPIO.LOW:
            pulse_count += 1
            while GPIO.input(coin_pin) == GPIO.LOW:
                pass  # Wait for coin to be removed from coin slot
            return pulse_count

if __name__ == "__main__":
    while True:
        pulse = get_pulse_count()
        print("pulse:", pulse)
        if pulse == 5:
            break