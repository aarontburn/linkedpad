import RPi.GPIO as GPIO
from Helper import log




key_map: dict[tuple[int, int], tuple[int, int]] = {}


KEYS = [row + col for row in ['H', "A", "B", "C", "D"] for col in ["0", "1", "2", "3"]]
ROW_PINS = [29, 31, 33, 35, 37] 
COL_PINS = list(reversed([32, 36, 38, 40]))


def setup_gpio() -> None:
    log("Initializing...")

    try:
        GPIO.setmode(GPIO.BOARD)
        
    except ValueError as e:      # Board is already initialized for some reason
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)


    for pin in ROW_PINS:
        GPIO.setup(pin, GPIO.OUT)


    for pin in COL_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        
    setup_keys()
    

    log("Finished initializing.")


def setup_keys() -> None:
    index = 0
    for row in ROW_PINS:
        for col in COL_PINS:
            key_map[(row, col)] = (row, col)
            index += 1
    

def gpio_listen() -> None:
    log("GPIO listener started.")

    while True:
        for row_pin in ROW_PINS:
            GPIO.output(row_pin, 0)
            for col_pin in COL_PINS:
                if GPIO.input(col_pin) == 0:
                    log(key_map[(row_pin, col_pin)]._row_col)
                
            GPIO.output(row_pin, 1)



def destroy_gpio() -> None:
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        setup_gpio()
        gpio_listen()
    except KeyboardInterrupt:
        destroy_gpio()