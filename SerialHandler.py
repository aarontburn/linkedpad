import serial
from log import log
import time
import json
import LEDHandler

_PORT: str = '/dev/ttyGS0'
_BAUD: int = 9600

_ser: serial.Serial = None
_is_connected = False

def init():
    _establish_serial()
    _attempt_connection()
    listen()

def _attempt_connection() -> None: 
    log('Connecting to PC...')
    
    while True:
        write('pi_ready', False)
        time.sleep(1)
        
        data: str = str(_ser.readline())[2:-3]
        if data == 'pc_ready':
            log('Successfully established connection with PC.')
            
            global _is_connected
            _is_connected = True
            return
        
        
def is_connected() -> bool:
    return _is_connected


def listen() -> None:
    log("Listening...")
    while True:
        try:
            data: str = str(_ser.readline())[2:-3]
            if data != '':
                _handle_events(data)
                
        except Exception:
            _establish_serial()


def _handle_events(event_string: str) -> None:
    split_str: list[str] = event_string.split(' ')
    match split_str[0]:
        case 'brightness':
            brightness: float = float(split_str[1])
            log('Brightness: ' + str(brightness))
            
        case 'rgb': 
            rgb: list[int] = json.loads(split_str[1])
            log("RGB:", rgb)
        
        case 'state':
            state: list[str] = json.loads(split_str[1])
            for row_col in state:
                LEDHandler.set_light(row_col, state[row_col])
        
        case _:
            log('No handler for: ' + split_str[0])


def write(data: str, out: bool = True) -> None:
    if _ser != None:
        if out:
            log("Sending " + str(data))
            
        try:
            _ser.write((str(data) + "\n").encode())
        except Exception:
            _establish_serial()
            _ser.write((str(data) + "\n").encode())
            


def _establish_serial() -> None:
    cleanup()
        
    global _ser
    _ser = serial.Serial(
        port=_PORT,
        baudrate = _BAUD,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,  
        timeout=0.25,
        rtscts=True
    )

def cleanup() -> None:
    if _ser != None:
        _ser.close()
        
    
if __name__ == '__main__':
    try:
        init()
        listen()
    except KeyboardInterrupt:
        cleanup()