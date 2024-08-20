import time
import ColorHandler
import DatabaseHandler
import SerialHandler
from log import log
import LEDHandler

_DEBOUNCE: int = 20


class Key:
    _currently_pressed: bool = False
    _last_press_milli = 0

    _input_pin: int
    _output_pin: int

    # Could be reduced to rowCol ('A3')
    _row: str
    _col: str

    def __init__(self, input_pin: int, output_pin: int, row_col: str) -> None:
        self._input_pin = input_pin
        self._output_pin = output_pin
        self._row = row_col[0]
        self._col = row_col[1]

    def handle_input(self, gpio_input_callback) -> None:
        if not self._handle_debounce():
            return

        is_down: bool = gpio_input_callback(self._input_pin) == 0
        
        if self._currently_pressed:
            if is_down:                 # Hold
                pass
                
            else:                       # Key Up
                self._currently_pressed = False
                
                if SerialHandler.is_connected():
                    if SerialHandler.in_linked_mode() == False:
                        LEDHandler.set_light(self._row + self._col, ColorHandler.OFF)
                    
                
                
        else:
            if is_down:                 # Key Down
                log("Down")
                
                if SerialHandler.is_connected():
                    if SerialHandler.in_linked_mode() == False:
                        LEDHandler.set_light(self._row + self._col, ColorHandler.WHITE)
                    SerialHandler.write(self._row + self._col)
                else:
                    DatabaseHandler.on_key_press(self._row, self._col)
                    
                self._currently_pressed = True
                
            else:                       # Inactive
                pass

    def _handle_debounce(self) -> bool:
        milli = round(time.time() * 1000)

        if milli < self._last_press_milli + _DEBOUNCE:
            return False    # Don't proceed

        self._last_press_milli = milli
        return True     # Proceed
