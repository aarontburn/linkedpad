from time import sleep
import board
import neopixel
import ColorHandler
from log import log

_local_state = {}

ROWS: list[str] = ['A', 'B', 'C', 'D']
MAX_COLS: int = 4

def build_light_map() -> dict[str, int]:
    rows: list[str] = ROWS * MAX_COLS

    out: dict[str, int] = {}

    col_index: int = -1

    for i in range(len(rows)):
        if rows[i] == ROWS[0]:
            col_index += 1

        out[rows[i] + str(col_index)] = i

    return out


LIGHT_MAP: dict[str, int] = build_light_map()
BRIGHTNESS: float = 0.15

GPIO = board.D18 	# pin 12
pixels = None


def init():
    log("Initializing LED Handler...")
    global pixels
    pixels = neopixel.NeoPixel(GPIO, len(LIGHT_MAP), brightness=BRIGHTNESS)

    log("LED Handling initialized.")
    
    if __name__ == "__main__":
        _loop()


def _loop(): # This should only be for debugging
    log("Beginning loop")
    while (True):
        set_light('A0', ColorHandler.WHITE)
        sleep(1)
        set_light('A0', ColorHandler.OFF)
        sleep(1)


def set_state(state):
    global _local_state
    _local_state = state
    
    for row_col in _local_state:
        set_light(row_col, _local_state[row_col])
    

def set_light(row_col: str, rgb: list[int, int, int]):
    log("Setting light at:", row_col, "(index " + str(LIGHT_MAP[row_col]) + ") to", rgb)
    _local_state[row_col] = rgb
    print(pixels)
    pixels[int(LIGHT_MAP[row_col])] = (rgb[0], rgb[1], rgb[2])
    
    
def cleanup() -> None:
    for row_col in LIGHT_MAP:
        pixels[LIGHT_MAP[row_col]] = ColorHandler.OFF
        

if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        cleanup()
        
    