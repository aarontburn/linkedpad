from Helper import pwd, log

OFF: list[int, int, int] = [0, 0, 0]
WHITE: list[int, int, int] = [255, 255, 255]
RED: list[int, int, int] = [255, 0, 0]
YELLOW: list[int, int, int] = [255, 255, 0]
GREEN: list[int, int, int] = [0, 255, 0]
BLUE: list[int, int, int] = [0, 0, 255]
VIOLET: list[int, int, int] = [125, 0, 255]


_DEFAULT_COLOR_SEQ: list[list[int, int, int]] = [WHITE, RED, YELLOW, GREEN, BLUE, VIOLET]

_COLOR_SEQ: list[list[int, int, int]] = _DEFAULT_COLOR_SEQ

_current_color_index = 0


def load_colors_from_storage():
    log("Loading saved colors...")
    with open(pwd() + "/colors.txt", "w+") as f:
        contents: str = f.read()
        
        if (contents == ''):
            pass # Ignore, leave _COLOR_SEQ as default
        else:
            rgb_list: list[list[int, int, int]] = map(hex_to_rgb, contents.split(" "))
            
            global _COLOR_SEQ
            _COLOR_SEQ = rgb_list
            
            log(_COLOR_SEQ)
        
    

# Default macro press color is white.
_macro_press_color: list[int, int, int] = WHITE

def set_macro_press_color(rgb: list[int, int, int]) -> None:
    global _macro_press_color
    _macro_press_color = rgb

def get_macro_press_color() -> list[int, int, int]:
    return _macro_press_color



def next_color() -> None:
    global _current_color_index
    
    _current_color_index += 1
    if _current_color_index > len(_COLOR_SEQ) - 1:
        _current_color_index = 0

def get_current_color() -> list[int, int, int]:
    return _COLOR_SEQ[_current_color_index]

def rgb_to_hex(rgb: list[int, int, int]) -> str:
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

def hex_to_rgb(hex: str) -> list[int, int, int]:
    return tuple(int(hex[1:][i:i+2], 16) for i in (0, 2, 4))

