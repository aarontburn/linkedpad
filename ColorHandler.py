OFF: list[int, int, int] = [0, 0, 0]
WHITE: list[int, int, int] = [255, 255, 255]
RED: list[int, int, int] = [255, 0, 0]
YELLOW: list[int, int, int] = [255, 255, 0]
GREEN: list[int, int, int] = [0, 255, 0]
BLUE: list[int, int, int] = [0, 0, 255]
VIOLET: list[int, int, int] = [125, 0, 255]

_COLOR_SEQ: list[list[int, int, int]] = [WHITE, RED, YELLOW, GREEN, BLUE, VIOLET]

_current_color_index = 0

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



