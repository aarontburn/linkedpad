from time import sleep
import board
import neopixel

OFF: tuple[int, int, int] = (0, 0, 0)

WHITE: tuple[int, int, int] = (255, 255, 255)
RED: tuple[int, int, int] = (255, 0, 0)
ORANGE: tuple[int, int, int] = (255, 165, 0)
YELLOW: tuple[int, int, int] = (255, 255, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
BLUE: tuple[int, int, int] = (0, 0, 255)
VIOLET: tuple[int, int, int] = (125, 0, 255)

COLOR_SEQ: list[tuple[int, int, int]] = [WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET]


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

GPIO: board.Pin = board.D18 	# pin 12

pixels: neopixel.NeoPixel = None
current_color_index = 0

def init():
    print("Initializing LED Handler...")
    global pixels
    pixels = neopixel.NeoPixel(GPIO, len(LIGHT_MAP), brightness=BRIGHTNESS)

    print("LED Handling initialized.")
    # _loop()


def _loop(): # This should only be for debugging
    print("Beginning loop")
    while (True):
        set_light(0, (255, 0, 0))
        sleep(1)
        set_light(0, (0, 0, 255))
        sleep(1)


def set_light(row_col: str, is_on: bool):
    print("Setting light at:", row_col, "(index " + str(LIGHT_MAP[row_col]) + ") to", get_current_color() if is_on else OFF)
    
    pixels[int(LIGHT_MAP[row_col])] = get_current_color() if is_on else OFF
    
    
    
def cleanup() -> None:
    for row_col in LIGHT_MAP:
        pixels[LIGHT_MAP[row_col]] = OFF
        

def next_color() -> None:
    global current_color_index
    
    current_color_index += 1
    if current_color_index > len(COLOR_SEQ) - 1:
        current_color_index = 0

def get_current_color() -> tuple[int, int, int]:
    return COLOR_SEQ[current_color_index]

if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        cleanup()
        
    