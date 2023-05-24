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

def reset_coin_value():
    global coin_value
    coin_value = 0

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
            coin_value += calculate_coin_value(counter)
            print("coin_value", coin_value)
            print(f"Pulse coming! {counter}")
            ts = time.time()

def secondFunction():
    global count
    global counting
    global counter
    while True:
        cts = ts + 2
        if cts < time.time():
            print(f"Counting looks like finished with {counter} pulses")
            count = 0
            counting = 0
            print("We process accepted the coins")

            # urllib2.urlopen is just for testing in my case, you can do whatever you want here, i just used this to test the functions
            if counter == 1:
                print("Counter 1")
            if counter == 2:
                print("Counter 2")
            if counter == 3:
                print("Counter 3")
            if counter == 4:
                print("Counter 4")
            if counter == 5:
                print("Counter 5")

            counter = 0
            count = 1
            print("Ready for the next coin")
            time.sleep(1)


def thirdFunction():
    while True:
        if counting == 0:
            reset_coin_value()
            global ts
            ts = time.time()
            time.sleep(1)


try:
    t1 = Thread(target=firstFunction)
    t2 = Thread(target=secondFunction)
    t3 = Thread(target=thirdFunction)

    t1.start()
    t2.start()
    t3.start()

except KeyboardInterrupt:
    t1.stop()
    t2.stop()
    t3.stop()
    GPIO.cleanup()