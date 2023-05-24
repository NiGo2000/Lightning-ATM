import RPi.GPIO as GPIO
import time
from threading import Thread

coin_pin = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(coin_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global count
global counting
global coin_value

counting = 0
coin_value = 0

# Coin value calculation function
def calculate_coin_value(pulse_count):
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

# Coin value reset function
def reset_coin_value():
    global coin_value
    coin_value = 0

# First pulse detection function
def firstFunction():
    global counter
    global ts
    global counting
    global coin_value
    count = 1
    counter = 0
    ts = time.time()
    while True:
        if count == 1:
            GPIO.wait_for_edge(coin_pin, GPIO.FALLING)
            counting = 1
            counter += 1
            print(f"Pulse coming! {counter}")
            ts = time.time()

# Second function for processing the pulse detection
def secondFunction():
    global count
    global counting
    global counter
    global coin_value
    while True:
        cts = ts + 0.1
        if cts < time.time():
            print(f"Counting looks like finished with {counter} pulses")
            count = 0
            counting = 0
            print("We process accepted the coins")
            coin_value += calculate_coin_value(counter)
            print(f"Coin value: {coin_value} €")

            counter = 0
            count = 1
            print("Ready for the next coin")
            time.sleep(1)

def get_cash():
    global coin_value
    return coin_value

try:
    t1 = Thread(target=firstFunction)
    t2 = Thread(target=secondFunction)
    t3 = Thread(target=get_cash)

    t1.start()
    t2.start()
    t3.start()

except KeyboardInterrupt:
    t1.stop()
    t2.stop()
    GPIO.cleanup()