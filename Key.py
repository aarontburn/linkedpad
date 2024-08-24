import time
import ColorHandler
import DatabaseHandler
import SerialHandler
from log import log
import LEDHandler


_DEBOUNCE: int = 50


class Key:
    _currently_pressed: bool = False
    _last_press_time = 0

    _row_pin: int
    _col_pin: int

    # Could be reduced to rowCol ('A3')
    _row: str
    _col: str

    def __init__(self, row_pin: int, col_pin: int, row_col: str) -> None:
        self._row_pin = row_pin
        self._col_pin = col_pin
        self._row = row_col[0]
        self._col = row_col[1]
        
        if row_col == 'H0':
            LEDHandler.set_light(row_col, ColorHandler.get_current_color())

    def handle_input(self, gpio_input_callback) -> None:
        if self._handle_debounce() == False:
            return

        is_down: bool = gpio_input_callback(self._col_pin) == 0
        
        if self._currently_pressed:
            if is_down:                 # Hold
                if SerialHandler.is_connected():
                    SerialHandler.write(self._row + self._col)

                
            else:                       # Key Up
                self._currently_pressed = False
                
                if SerialHandler.is_connected():
                    if SerialHandler.in_linked_mode() == False:
                        LEDHandler.set_light(self._row + self._col, ColorHandler.OFF)
                    
                
                
        else:
            if is_down:                 # Key Down
                log("Down", self._row, self._col)
                
                if SerialHandler.is_connected():
                    if SerialHandler.in_linked_mode() == False:
                        LEDHandler.set_light(self._row + self._col, ColorHandler.WHITE)
                    SerialHandler.write(self._row + self._col)
                else:
                    if (self._row == 'H'):
                        match self._col:
                            case '0':
                                ColorHandler.next_color()
                                LEDHandler.set_light('H0', ColorHandler.get_current_color())
                            case '1':
                                LEDHandler.set_brightness(0.1)
                                pass
                            case '2':
                                pass
                            case '3':
                                pass
                        
                        
                        DatabaseHandler.on_key_press(self._row, self._col)
                    
                self._currently_pressed = True
                
            else:                       # Inactive
                pass
        

    def _handle_debounce(self) -> bool:
        milliseconds = round(time.time() * 1000)

        if milliseconds < self._last_press_time + _DEBOUNCE:
            return False    # Don't proceed

        self._last_press_time = milliseconds
        return True     # Proceed
