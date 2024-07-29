import RPi.GPIO as GPIO
import DatabaseHandler

# GPIO setup
pin = 7
pin1 = 37

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, GPIO.LOW)

def gpio_loop():
    while True:
        if GPIO.input(pin) == 0:
            DatabaseHandler.on_key_press('A', '3')

def destroy_gpio():
    GPIO.cleanup()
