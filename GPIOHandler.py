import RPi.GPIO as GPIO
import time
from Key import Key
from log import log




key_map: dict[str, Key] = {}

ROW_PINS = [29, 31, 33, 35, 37]
COL_PINS = [40, 38, 36, 32]
KEYS = [row + col for row in ["A", "B", "C", "D"] for col in ["0", "1", "2", "3"]]



def setup_gpio() -> None:
    log("Initializing GPIO handler...")

    try:
        GPIO.setmode(GPIO.BOARD)
        
    except ValueError as e:      # Board is already initialized for some reason
        destroy_gpio()
        GPIO.setmode(GPIO.BOARD)


    for pin in COL_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


    for pin in ROW_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        

    log("GPIO initialization finished.")


def setup_keys() -> None:
    print("here")
    index = 0
    
    
    print(len(COL_PINS))
    print(COL_PINS)
    print(ROW_PINS)
    
    for i in range(len(COL_PINS)):
        
        col = COL_PINS[i]
        for j in range(len(ROW_PINS)):
            print(i, j)
            row = ROW_PINS[j]
            # key_map[KEYS[index]] = Key(row, col, KEYS[index])
            i += 1
            print(col, row)
             
    
            
    print("here 1")
    
    print(key_map)

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
    except Exception:
        destroy_gpio()