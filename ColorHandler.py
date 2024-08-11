


OFF: list[int, int, int] = [0, 0, 0]
WHITE: list[int, int, int] = [255, 255, 255]
RED: list[int, int, int] = [255, 0, 0]
ORANGE: list[int, int, int] = [255, 165, 0]
YELLOW: list[int, int, int] = [255, 255, 0]
GREEN: list[int, int, int] = [0, 255, 0]
BLUE: list[int, int, int] = [0, 0, 255]
VIOLET: list[int, int, int] = [125, 0, 255]

_COLOR_SEQ: list[tuple[int, int, int]] = [WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET]

_current_color_index = 0

def next_color() -> None:
    global _current_color_index
    
    _current_color_index += 1
    if _current_color_index > len(_COLOR_SEQ) - 1:
        _current_color_index = 0

def get_current_color() -> list[int, int, int]:
    return _COLOR_SEQ[_current_color_index]

def rgb_to_hex(rgb: list[int, int, int]) -> str:
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])



