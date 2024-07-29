import DatabaseHandler


class Key:
    _pressed: bool = False

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

    def handle_input(self, gpio_input):
        if self._pressed == True:
            if gpio_input(self._input_pin) == 0:  # Hold
                pass
                
            else:                               # Key Up
                self._pressed = False
                
        else:
            if gpio_input(self._input_pin) == 0:  # Key Down
                print("Down")
                if self._input_pin == 11:
                    DatabaseHandler.test()
                else:
                    DatabaseHandler.on_key_press(self._row, self._col)
                self._pressed = True
                
            else:                               # Inactive
                pass
