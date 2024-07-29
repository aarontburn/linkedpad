import RPi.GPIO as GPIO
import time
from Key import Key




key_map: dict[str, Key] = {}

INPUT_PINS = [3, 11]
OUTPUT_PINS = [5, 13]


def setup_gpio():
    print("Initializing GPIO handler...")

    GPIO.setmode(GPIO.BOARD)
    
    for pin in INPUT_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    for pin in OUTPUT_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
    setup_keys()

    print("GPIO initialization finished.")

def setup_keys() -> None:
    key_map['A3'] = Key(3, 5, "A3")
    key_map['D0'] = Key(11, 13, "D0")



def gpio_listen():
    print("GPIO listener started.")

    while True:
        for row_col in key_map:
            key_map[row_col].handle_input(GPIO.input)


def destroy_gpio():
    GPIO.cleanup()
