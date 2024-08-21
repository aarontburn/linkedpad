import serial
from log import log
import time
import json
import LEDHandler
from main import _start_thread, _get_temp
import subprocess

_PORT: str = '/dev/ttyGS0'
_BAUD: int = 9600

_ser: serial.Serial = None
_is_connected = False
_is_exiting = False
_linked_mode = False 

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
            _start_thread(maintain_connection)
            LEDHandler.cleanup()
            
            global _is_connected
            _is_connected = True
            return
        
def maintain_connection() -> None:
    while True:
        if _is_exiting:
            break
        
        write('pi_ready', False)
        write('temp ' + str(_get_temp()), False)
        time.sleep(3)
        
        
def is_connected() -> bool:
    return _is_connected


def in_linked_mode() -> bool:
    return _linked_mode


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
            LEDHandler.set_brightness(brightness)
            
        case 'selected-color': 
            rgb: list[int] = json.loads(split_str[1])
            log("Selected color:", rgb)
            LEDHandler.set_light('H0', rgb)
        
        case 'change':
            row_col: str = split_str[1]
            rgb: list[int] = json.loads(split_str[2])
            LEDHandler.set_light(row_col, rgb)
        
        case 'linked-mode':
            global _linked_mode
            _linked_mode = int(split_str[1]) == 1
            
            log("linked-mode:", split_str[1])
            
        case 'pc_ready': # Ignore?
            pass
        
        case 'wifi-setup':
            wifi_ssid: str = split_str[1]
            wifi_pass: str = split_str[2]
            
            log("Attempting wifi connection with " + wifi_ssid + " and " + wifi_pass)
            
            output = subprocess.call(['sudo', 'raspi-config', 'nonint', 'do_wifi_ssid_passphrase', wifi_ssid, wifi_pass], shell=True) 
            log(output)
            
        
        case _:
            log('No handler for: ' + split_str[0])


def write(data: str, out: bool = True) -> None:
    if _ser != None:
        if out:
            log("Sending " + str(data))
            
        try:
            _ser.write((str(data) + "\n").encode())
        except Exception as e:
            log(e)
            
            


def _establish_serial() -> None:
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
    global _is_exiting
    _is_exiting = True
    
    if _ser != None:
        write('pi_exit')
        time.sleep(0.1)
        _ser.close()
        
    
if __name__ == '__main__':
    try:
        init()
        listen()
    except KeyboardInterrupt:
        cleanup()