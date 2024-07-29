import RPi.GPIO as GPIO
import DatabaseHandler
import time

# GPIO setup
INPUT_PIN = 3
OUTPUT_PIN = 5

def setup_gpio():
    print("Initializing GPIO handler...")
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(OUTPUT_PIN, GPIO.OUT)
    GPIO.output(OUTPUT_PIN, GPIO.LOW)
    
    print("GPIO initialization finished.")

def gpio_listen():
    print("GPIO listener started.")
    while True:
        if GPIO.input(INPUT_PIN) == 0:
            DatabaseHandler.on_key_press('A', '3')
            _milli()

def destroy_gpio():
    GPIO.cleanup()


def _milli():
    return round(time.time() * 1000)