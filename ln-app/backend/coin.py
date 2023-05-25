from asyncio import Lock
import RPi.GPIO as GPIO
import time
from threading import Thread, Lock

coin_pin = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(coin_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

coin_value = 0
pulse_count = 0
lock = Lock()

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

def get_cash():
    global coin_value
    with lock:
        return coin_value

# Coin value reset function
def reset_coin_value():
    global coin_value
    with lock:
        coin_value = 0

# Pulse detection function
def pulse_detection():
    global pulse_count
    while True:
        GPIO.wait_for_edge(coin_pin, GPIO.FALLING)
        with lock:
            pulse_count += 1

# Coin value conversion function
def coin_value_conversion():
    global pulse_count
    global coin_value
    while True:
        time.sleep(1)  # Adjust the sleep interval as needed
        with lock:
            if pulse_count > 0:
                coin_value += calculate_coin_value(pulse_count)
                print(f"Coins detected: {pulse_count}")
                print(f"Current cash: {coin_value}")
                pulse_count = 0

# Start the pulse detection thread
t1 = Thread(target=pulse_detection)
t1.start()

# Start the coin value conversion thread
t2 = Thread(target=coin_value_conversion)
t2.start()