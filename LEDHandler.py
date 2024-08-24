from time import sleep
import board
import neopixel
import ColorHandler
from log import log


ROWS: list[str] = ['H', 'A', 'B', 'C', 'D']
MAX_COLS: int = 4

def build_light_map() -> dict[str, int]:
    rows: list[str] = (ROWS + list(reversed(ROWS.copy()))) * int(MAX_COLS / 2)

    out: dict[str, int] = {}
    pos_index: int = len(rows) - 1
    col_index: int = -1
    for i in range(len(rows)):
        if i % 5 == 0:
            col_index += 1

        out[rows[i] + str(col_index)] = pos_index
        pos_index -= 1
        
    return out

_linked_mode_state = {}


brightness_scale = 0.5 # Half brightness

LIGHT_MAP: dict[str, int] = build_light_map()

GPIO = board.D18 	# pin 12
pixels = None


def init():
    log("Initializing LED Handler...")
    global pixels
    pixels = neopixel.NeoPixel(GPIO, len(LIGHT_MAP), brightness=brightness_scale)
    
    
    log("LED Handling initialized.")
    
    


def set_brightness(val: float) -> None:
    pixels.brightness = val * brightness_scale
    
    

def linked_mode_toggle(in_linked_mode: bool) -> None: 
    if in_linked_mode:
        for row_col in _linked_mode_state:
            set_light(row_col, _linked_mode_state[row_col])
            
    else:
        for i in range(len(LIGHT_MAP)):
            pixels[i] = (0, 0, 0)
            
        
        

def set_light(row_col: str, rgb: list[int, int, int]):
    _linked_mode_state[row_col] = rgb
    
    # log("Setting light at:", row_col, "(index " + str(LIGHT_MAP[row_col]) + ") to", tuple(rgb))
    pixels[int(LIGHT_MAP[row_col])] = (rgb[0], rgb[1], rgb[2])
    
    
def cleanup() -> None:
    for row_col in LIGHT_MAP:
        pixels[LIGHT_MAP[row_col]] = ColorHandler.OFF
        

if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        cleanup()
        
    