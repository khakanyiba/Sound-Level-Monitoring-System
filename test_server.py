import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

print("Listening for raw input on GPIO17...")
try:
    while True:
        value = GPIO.input(17)
        print(f"Sensor value: {value}")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
