import time
import ColorHandler
import DatabaseHandler
import SerialHandler
import LEDHandler


_DEBOUNCE: int = 50
_REPEAT_DELAY: int = 250


class Key:
    _currently_pressed: bool = False
    _last_press_time = 0
    _down_time = 0

    _row_pin: int
    _col_pin: int

    _row_col: str

    def __init__(self, row_pin: int, col_pin: int, row_col: str) -> None:
        self._row_pin = row_pin
        self._col_pin = col_pin
        self._row_col = row_col
        

    def handle_input(self, gpio_input_callback) -> None:
        if self._handle_debounce() == False:
            return

        is_down: bool = gpio_input_callback(self._col_pin) == 0
        
        if self._currently_pressed:
            if is_down:                 # Hold
                if SerialHandler.is_connected():
                    if SerialHandler.in_linked_mode() == False:
                        if self._wait_for_repeat_delay():
                           SerialHandler.write(self._row_col + " hold")
                           
                
            else:                       # Key Up
                self._currently_pressed = False
                
                
                if SerialHandler.is_connected():
                    SerialHandler.write(self._row_col + " up")
                    
                    if SerialHandler.in_linked_mode() == False:
                        LEDHandler.set_light(self._row_col, ColorHandler.OFF)
                        
                else:
                    if (self._row_col[0] == 'H'):
                        match self._row_col[1]:
                            case '0':
                                ColorHandler.next_color()
                                LEDHandler.set_light('H0', ColorHandler.get_current_color())
                            case '1':
                                LEDHandler.set_brightness()
                                LEDHandler.set_light(self._row_col, ColorHandler.OFF)
                                
                            case '2':
                                DatabaseHandler.reset()
                                DatabaseHandler.recalibrate()
                                
                                LEDHandler.set_light(self._row_col, ColorHandler.OFF)
                            case '3':
                                pass
                    
                
                
        else:
            if is_down:                 # Key Down
                self._down_time = self._ms()
                
                if SerialHandler.is_connected():
                    if SerialHandler.in_linked_mode() == False:
                        LEDHandler.set_light(self._row_col, ColorHandler.WHITE)
                    SerialHandler.write(self._row_col + " down")
                else:
                    if (self._row_col[0] == 'H'):
                        match self._row_col[1]:
                            case '0':
                                ColorHandler.next_color()
                                LEDHandler.set_light('H0', ColorHandler.get_current_color())
                            case '1':
                                LEDHandler.set_brightness()
                                LEDHandler.set_light(self._row_col, ColorHandler.YELLOW)
                            case '2':
                                DatabaseHandler.reset()
                                DatabaseHandler.recalibrate()
                                LEDHandler.set_light(self._row_col, ColorHandler.RED)
                            case '3':
                                pass
                    else:
                        DatabaseHandler.on_key_press(self._row_col)
                    
                self._currently_pressed = True
                
            else:                       # Inactive
                pass
        

    def _handle_debounce(self) -> bool:
        ms = self._ms()

        if ms < self._last_press_time + _DEBOUNCE:
            return False    # Don't proceed

        self._last_press_time = ms
        return True     # Proceed


    def _wait_for_repeat_delay(self) -> bool:
        return self._ms() > self._down_time + _REPEAT_DELAY
    
    
    def _ms(self):
        return round(time.time() * 1000)