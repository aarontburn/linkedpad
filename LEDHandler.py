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
_DEFAULT_BRIGHTNESS = _BRIGHTNESS_STEPS[1] # 0.1



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

def _build_default_state() -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    
    for row in ROWS:
        for col in range(MAX_COLS):
            out[str(row) + str(col)] = ColorHandler.OFF
            
    return out
        
    



_linked_mode_state = _build_default_state()




LIGHT_MAP: dict[str, int] = _build_light_map()

GPIO = board.D18 	# pin 12
pixels = None


def init():
    log("Initializing...")
    WifiHandler.add_listener(_wifi_listener)
    
    global pixels
    pixels = neopixel.NeoPixel(GPIO, len(LIGHT_MAP), brightness=_DEFAULT_BRIGHTNESS * _BRIGHTNESS_SCALE)
    
    
    log("Finished initializing.")

queue = Queue()
def _wifi_listener(is_connected: bool) -> None:
    global queue
    
    if SerialHandler.is_connected() == False:
        if is_connected:
            cleanup()
            queue.put_nowait(1)
            
        else: # Disconnected, but not connected to pc.
            cleanup()
            
            queue = Queue()
            start_thread(do_error_pattern, args=(queue,))
            
            
            

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
        for row_col in _linked_mode_state:
            set_light(row_col, _linked_mode_state[row_col])
            
        # set_light('H0', ColorHandler.get_current_color())
    else:
        for i in range(len(LIGHT_MAP)):
            pixels[i] = tuple(ColorHandler.OFF)
            
        
        

def set_light(row_col: str, rgb: list[int, int, int], b: bool = True):
    if (str(row_col[0]) not in ROWS or str(row_col[1]) not in ['0', '1', '2', '3']):
        log("Invalid row_col passed: " + row_col)
        return
    
    
    
    _linked_mode_state[row_col] = rgb
    
    if b:
        pixels[int(LIGHT_MAP[row_col])] = (rgb[0], rgb[1], rgb[2])
    
    
def cleanup() -> None:
    for row_col in LIGHT_MAP:
        pixels[LIGHT_MAP[row_col]] = tuple(ColorHandler.OFF)



_boot_flag: int = 0

def alert_boot_process(flag: int) -> None:
    global _boot_flag
    _boot_flag = flag

    

def do_loading_pattern(queue: Queue) -> None:
    pattern: list[str] = ['A0', 'A1', 'A2', 'A3', 'B3', 'C3', 'D3', 'D2', 'D1', 'D0', 'C0', 'B0']
    set_brightness(0.3)
    
    while queue.qsize() == 0:
        for row_col in pattern:
            if queue.qsize() > 0:
                break
            
            pixels[int(LIGHT_MAP[row_col])] = tuple(ColorHandler.WHITE)
            sleep(0.25)
            
            if queue.qsize() > 0:
                break
            
            pixels[int(LIGHT_MAP[row_col])] = tuple(ColorHandler.OFF)

            
def do_error_pattern(queue: Queue) -> None:
    pattern: list[str] = ['A0', 'A1', 'A2', 'A3', 'B3', 'C3', 'D3', 'D2', 'D1', 'D0', 'C0', 'B0']
    
    while queue.qsize() == 0:
        for row_col in pattern:
            if queue.qsize() > 0:
                break
            pixels[int(LIGHT_MAP[row_col])] = tuple(ColorHandler.RED)

        sleep(0.5)
        
        for row_col in pattern:
            if queue.qsize() > 0:
                break
            pixels[int(LIGHT_MAP[row_col])] = tuple(ColorHandler.OFF)
        
        sleep(0.5)
        
            
        
        

if __name__ == "__main__":
    try:
        init()
        do_error_pattern()
    except KeyboardInterrupt:
        cleanup()
        
    