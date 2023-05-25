import threading
import RPi.GPIO as GPIO

coin_value = 0
lock = threading.Lock()
pulse_pin = 15

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Setup Pulse Pin
GPIO.setup(pulse_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

# Function to get the current cash
def get_cash():
    global coin_value
    return coin_value

# Function to reset coin_value to 0
def reset_cash():
    global coin_value
    coin_value = 0

# Function to read pulses
def read_pulse():
    pulse_count = 0

    # Wait for pulse to start (falling edge)
    GPIO.wait_for_edge(pulse_pin, GPIO.FALLING)

    # Count pulses
    while GPIO.input(pulse_pin) == GPIO.LOW:
        pulse_count += 1

    return pulse_count

# Function to process pulses and update coin_value
def process_pulse():
    while True:
        pulse_count = read_pulse()
        with lock:
            coin_value += calculate_coin_value(pulse_count)

# Start the pulse processing thread
pulse_thread = threading.Thread(target=process_pulse)
pulse_thread.daemon = True
pulse_thread.start()