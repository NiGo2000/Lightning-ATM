import RPi.GPIO as GPIO
import time
from threading import Thread

# GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def firstFunction():
    global counter
    global ts
    global counting
    count = 1
    counter = 0
    ts = time.time()
    while True:
        if count == 1:
            GPIO.wait_for_edge(6, GPIO.FALLING)
            counting = 1
            counter += 1
            print(f"Pulse comming ! {counter}")
            ts = time.time()

if __name__ == "__main__":
    firstFunction()