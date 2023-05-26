import os
import RPi.GPIO as GPIO
import time
from threading import Thread, Lock
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
coin_pin = os.getenv("coin_pin")

GPIO.setmode(GPIO.BCM)
GPIO.setup(coin_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global ts
global coin_value
global pulse_count

coin_value = 0
pulse_count = 0
lock = Lock()

# Coin value calculation function
def calculate_coin_value(pulse_count):
    if pulse_count == 2:
        return round(0.05, 2)
    elif pulse_count == 3:
        return round(0.10, 2)
    elif pulse_count == 4:
        return round(0.20, 2)
    elif pulse_count == 5:
        return round(0.50, 2)
    elif pulse_count == 6:
        return round(1.00, 2)
    elif pulse_count == 7:
        return round(2.00, 2)
    else:
        return 0.0

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
    global ts
    ts = time.time()
    while True:
        GPIO.wait_for_edge(coin_pin, GPIO.FALLING)
        with lock:
            pulse_count += 1
            ts = time.time()

# Coin value conversion function
def coin_value_conversion():
    global pulse_count
    global coin_value
    global ts
    while True:
        with lock:
            cts = ts + 0.5
            if cts < time.time():
                if pulse_count >= 2:
                    coin_value += calculate_coin_value(pulse_count)
                    pulse_count = 0

# Start the pulse detection thread
t1 = Thread(target=pulse_detection)
t1.start()

# Start the coin value conversion thread
t2 = Thread(target=coin_value_conversion)
t2.start()