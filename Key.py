import time
# import ColorHandler
# import DatabaseHandler
# import SerialHandler
from log import log
# import LEDHandler
import RPi.GPIO as GPIO


_DEBOUNCE: int = 20


class Key:
    _currently_pressed: bool = False
    _last_press_time = 0

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
        
        # print(gpio_input_callback(self._input_pin))
        GPIO.output(self._output_pin, 0)
        # if not self._handle_debounce():
        #     return

        is_down: bool = gpio_input_callback(self._input_pin) == 0
        
        if self._currently_pressed:
            if is_down:                 # Hold
                pass
                
            else:                       # Key Up
                self._currently_pressed = False
                
                # if SerialHandler.is_connected():
                #     if SerialHandler.in_linked_mode() == False:
                #         LEDHandler.set_light(self._row + self._col, ColorHandler.OFF)
                    
                
                
        else:
            if is_down:                 # Key Down
                log("Down", self._row, self._col)
                log(self)
                
                # if SerialHandler.is_connected():
                #     if SerialHandler.in_linked_mode() == False:
                #         LEDHandler.set_light(self._row + self._col, ColorHandler.WHITE)
                #     SerialHandler.write(self._row + self._col)
                # else:
                #     DatabaseHandler.on_key_press(self._row, self._col)
                    
                self._currently_pressed = True
                
            else:                       # Inactive
                pass
        GPIO.output(self._output_pin, 1)
        

    def _handle_debounce(self) -> bool:
        milliseconds = round(time.time() * 1000)

        if milliseconds < self._last_press_time + _DEBOUNCE:
            return False    # Don't proceed

        self._last_press_time = milliseconds
        return True     # Proceed
