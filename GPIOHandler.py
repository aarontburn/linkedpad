import RPi.GPIO as GPIO
import time
from Key import Key
from log import log




key_map: dict[str, Key] = {}

# ROW_PINS = [29, 31, 33, 35, 37]
# COL_PINS = [40, 38, 36, 32]



KEYS = [row + col for row in ['H', "A", "B", "C", "D"] for col in ["0", "1", "2", "3"]]
ROW_PINS = [37, 35, 33, 31, 29] 
COL_PINS = [7, 11, 13]





def setup_gpio() -> None:
    log("Initializing GPIO handler...")

    try:
        GPIO.setmode(GPIO.BOARD)
        
    except ValueError as e:      # Board is already initialized for some reason
        destroy_gpio()
        GPIO.setmode(GPIO.BOARD)


    for pin in ROW_PINS:
        GPIO.setup(pin, GPIO.OUT)


    for pin in COL_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        

    log("GPIO initialization finished.")


def setup_keys() -> None:
    index = 0
    for i in range(len(ROW_PINS)):
        col = ROW_PINS[i]
        for j in range(len(COL_PINS)):
            row = COL_PINS[j]
            key_map[KEYS[i]] = Key(row, col, KEYS[i])
            index += 1

            
    

def gpio_listen() -> None:
    log("GPIO listener started.")

    while True:
        for row_col in key_map:
            key_map[row_col].handle_input(GPIO.input)


def destroy_gpio() -> None:
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        setup_keys()
        setup_gpio()
        gpio_listen()
    except KeyboardInterrupt:
        destroy_gpio()