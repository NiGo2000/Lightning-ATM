import RPi.GPIO as GPIO

coin_pin = 6
pulse_count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(coin_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def coin_callback(channel):
    global pulse_count
    pulse_count += 1
    print("Pulse detected:", pulse_count)


def main():
    GPIO.add_event_detect(coin_pin, GPIO.FALLING, callback=coin_callback, bouncetime=300)

    try:
        while True:
            pass  # Hauptprogramm läuft weiter

    except KeyboardInterrupt:
        print("Programm abgebrochen")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()