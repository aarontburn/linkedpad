from time import sleep
import board
import neopixel


OFF: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)


MAX_COLS = 4

def build_light_map() -> dict[str, int]:
    rows: list[str] = ["H", 'A', 'B', 'C', 'D'] * MAX_COLS

    out: dict[str, int] = {}

    col_index: int = -1

    for i in range(len(rows)):
        if rows[i] == "H":
            col_index += 1

        out[rows[i] + str(col_index)] = i

    return out


LIGHT_MAP: dict[str, int] = build_light_map()

GPIO = board.D18 	# pin 12

pixels = None

def init():
    print("Initializing LED Handler...")
    global pixels
    pixels = neopixel.NeoPixel(GPIO, len(LIGHT_MAP))

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
    print("Setting light at:", row_col, "(index" + str(LIGHT_MAP[row_col]) + ") to", is_on)
    
    pixels[LIGHT_MAP[row_col]] = WHITE if is_on else OFF
    
    
    
def cleanup() -> None:
    for row_col in LIGHT_MAP:
        pixels[LIGHT_MAP[row_col]] = WHITE
        
        
    







if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        cleanup()
        
    