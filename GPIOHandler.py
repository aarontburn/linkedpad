import RPi.GPIO as GPIO
import time
from Key import Key
from log import log




key_map: dict[str, Key] = {}

INPUT_PINS = [38]
OUTPUT_PINS = [36]


def setup_gpio() -> None:
    log("Initializing GPIO handler...")

    try:
        GPIO.setmode(GPIO.BOARD)
    except ValueError: # Board is already initialized for some reason
        destroy_gpio()
        GPIO.setmode(GPIO.BOARD)


    for pin in INPUT_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        
    for pin in OUTPUT_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
    setup_keys()

    log("GPIO initialization finished.")

def setup_keys() -> None:
    key_map['A0'] = Key(38, 36, "A0")



def gpio_listen() -> None:
    log("GPIO listener started.")

    while True:
        for row_col in key_map:
            key_map[row_col].handle_input(GPIO.input)


def destroy_gpio() -> None:
    GPIO.cleanup()
