from time import sleep
import board
import neopixel
import ColorHandler
from Helper import log, start_thread
import SerialHandler
import WifiHandler
from queue import Queue

_BRIGHTNESS_STEPS = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
_BRIGHTNESS_SCALE = 0.5 # Half brightness
_brightness_index = 1
_DEFAULT_BRIGHTNESS = _BRIGHTNESS_STEPS[2] # 0.2



ROWS: list[str] = ['H', 'A', 'B', 'C', 'D']
MAX_COLS: int = 4

def _build_light_map() -> dict[str, int]:
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

    


LIGHT_MAP: dict[str, int] = _build_light_map()

GPIO = board.D18 	# pin 12
pixels = None


def init():
    log("Initializing...")
    WifiHandler.add_listener(_wifi_listener)
    
    global pixels
    pixels = neopixel.NeoPixel(GPIO, len(LIGHT_MAP), brightness=_DEFAULT_BRIGHTNESS * _BRIGHTNESS_SCALE)
    
    log("Finished initializing.")


def _wifi_listener(is_connected: bool) -> None:
    if SerialHandler.is_connected() == False:
        if is_connected:
            cleanup()
            set_light("H3", ColorHandler.OFF)
            
        else: # Disconnected, but not connected to pc.
            cleanup()
            set_light("H3", ColorHandler.RED)
            
            
            

def set_brightness(val: float = None) -> None:
    if val is None:
        global _brightness_index
        _brightness_index += 1
        
        if _brightness_index >= len(_BRIGHTNESS_STEPS):
            _brightness_index = 0
        
        val = _BRIGHTNESS_STEPS[_brightness_index]

    pixels.brightness = val * _BRIGHTNESS_SCALE
    
    

def linked_mode_toggle(in_linked_mode: bool) -> None: 
    if in_linked_mode:
        pass

    else:
        for i in range(len(LIGHT_MAP)):
            pixels[i] = tuple(ColorHandler.OFF)
            
        
        

def set_light(row_col: str, rgb: list[int, int, int], b: bool = True):
    if (str(row_col[0]) not in ROWS or str(row_col[1]) not in ['0', '1', '2', '3']):
        log("Invalid row_col passed: " + row_col)
        return
    
    if b:
        pixels[int(LIGHT_MAP[row_col])] = (rgb[0], rgb[1], rgb[2])
    
    
def cleanup() -> None:
    for row_col in LIGHT_MAP:
        pixels[LIGHT_MAP[row_col]] = tuple(ColorHandler.OFF)



        
        

if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        cleanup()
        
    