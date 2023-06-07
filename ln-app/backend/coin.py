import os
import RPi.GPIO as GPIO
import time
from threading import Thread, Lock

# coin_pin variable stores the GPIO pin number (15) for the coin sensor
coin_pin = 15

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up the coin_pin as an input with pull-up resistor enabled
GPIO.setup(coin_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # configures the coin_pin as an input with a pull-up resistor enabled

# Declare global variables
global ts
global coin_value
global pulse_count

# Initialize coin_value and pulse_count variables
coin_value = 0
pulse_count = 0

# Create a lock object for thread safety
lock = Lock()

# Coin value calculation function
def calculate_coin_value(pulse_count):
    # Determine the value of the coins based on the pulse count
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
    # Declare global variable
    global coin_value

    # Acquire a lock to ensure thread safety
    with lock:
        return coin_value # Return the current value of the coins

# Coin value reset function
def reset_coin_value():
    # Declare global variable
    global coin_value

    # Acquire a lock to ensure thread safety
    with lock:
        coin_value = 0 # Reset the value of the coins to zero

# Pulse detection function
def pulse_detection():
    # Declare global variables
    global pulse_count
    global ts

    # Set the initial timestamp
    ts = time.time()

    # Continuously detect pulses
    while True:
        # Wait for a falling edge on the coin_pin GPIO
        GPIO.wait_for_edge(coin_pin, GPIO.FALLING)
        # Acquire a lock to ensure thread safety
        with lock:
            # Increment the pulse count
            pulse_count += 1
             # Update the timestamp to the current time
            ts = time.time()

# Coin value conversion function
def coin_value_conversion():
    # Declare global variables
    global pulse_count
    global coin_value
    global ts

    # Continuously run the conversion process
    while True:
        # Acquire a lock to ensure thread safety
        with lock:
            # Calculate the current timestamp with a small offset
            cts = ts + 0.5
            # Check if the current timestamp is in the past
            if cts < time.time():
                # Check if there have been at least 2 pulses
                if pulse_count >= 2:
                    # Calculate the value of the coins based on the pulse count
                    coin_value += calculate_coin_value(pulse_count)

                    # Reset the pulse count to zero
                    pulse_count = 0

# Start the pulse detection thread
t1 = Thread(target=pulse_detection)
t1.start()

# Start the coin value conversion thread
t2 = Thread(target=coin_value_conversion)
t2.start()