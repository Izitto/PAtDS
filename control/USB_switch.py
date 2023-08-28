# getting the main GPIO libraly
import RPi.GPIO as GPIO
# getting the time libraly
from time import sleep
def run():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    pins = [18,27,22,23]
    #pins = [23]
    GPIO.setup(pins, GPIO.OUT)
    GPIO.output(23, 1)
    sleep(0.15)
    GPIO.output(23, 0)
    GPIO.cleanup()