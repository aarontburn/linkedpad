import serial
import time
import json
import LEDHandler
from Helper import start_thread, get_temp, log
from subprocess import run
import LEDHandler
import ColorHandler
import WifiHandler
import DatabaseHandler

_PORT: str = '/dev/ttyGS0'
_BAUD: int = 9600

_ser: serial.Serial = None
_is_connected = False
_is_exiting = False
_linked_mode = True # By default, we are in linked-mode 

def init():
    log('Initializing...')
    _establish_serial()
    _attempt_connection()
    listen()
    log('Finished initializing.')

def _attempt_connection() -> None: 
    log('Connecting to PC...')
    
    while True:
        write('pi_ready', False)
        time.sleep(1)
        
        data: str = str(_ser.readline())[2:-3]
        if data == 'pc_ready':
            _on_pc_connection()
            return
        
def maintain_connection() -> None:
    if _is_connected:
        log("Maintaining PC Connection...")
    while _is_connected:
        if _is_exiting:
            break
        
        write('pi_ready', False)
        write(_get_device_status(), False)
        time.sleep(3)
        
        
def is_connected() -> bool:
    return _is_connected


def in_linked_mode() -> bool:
    return _linked_mode


def listen() -> None:
    log("Listening...")
    while _is_connected:
        data: str = str(_ser.readline())[2:-3]
        if data != '':
            _handle_events(data)
                

def _handle_events(event_string: str) -> None:
    split_str: list[str] = event_string.split(' ')
    global _linked_mode
    global _is_connected
    
    
    match split_str[0]:
        case 'brightness':
            brightness: float = float(split_str[1])
            LEDHandler.set_brightness(brightness)
            
        case 'selected-color': 
            rgb: list[int] = json.loads(split_str[1])
            log("Selected color:", rgb)
            
            if _linked_mode:
                LEDHandler.set_light('H0', rgb)
        
        case 'change':
            row_col: str = split_str[1]
            rgb: list[int] = json.loads(split_str[2])
            LEDHandler.set_light(row_col, rgb, _linked_mode)
        
        case 'linked-mode':
            log("linked-mode:", split_str[1])
            
            if _linked_mode:
                LEDHandler.set_light('H0', json.loads(split_str[2]))
                
                
            _linked_mode = int(split_str[1]) == 1
            LEDHandler.linked_mode_toggle(_linked_mode)
            

            
        case 'pc_ready': # Ignore?
            if _is_connected == False:
                _on_pc_connection()
            pass
        
        case 'pc_exit':
            if _is_connected == False:
                return
            
            log("PC Exiting...")
            
            
            _is_connected = False
            _linked_mode = True
            for row_col in LEDHandler.LIGHT_MAP:
                LEDHandler.set_light(row_col, ColorHandler.OFF)
            
            LEDHandler.set_brightness(LEDHandler._DEFAULT_BRIGHTNESS)
            LEDHandler.alert_boot_process(0)
            start_thread(LEDHandler.do_loading_pattern)
            DatabaseHandler.init_db()
            LEDHandler.alert_boot_process(1)
            
            start_thread(DatabaseHandler.db_listen)
            init()

            pass
        
        case 'wifi-setup':
            wifi_ssid: str = split_str[1]
            wifi_pass: str = split_str[2]
            
            start_thread(_attempt_wifi, (wifi_ssid, wifi_pass))
            
        case 'reset':
            for row_col in LEDHandler.LIGHT_MAP:
                if row_col[0] != 'H':
                    LEDHandler.set_light(row_col, ColorHandler.OFF)
        
        case 'macro-press-color':
            rgb: list[int] = json.loads(split_str[1])
            ColorHandler.set_macro_press_color(rgb)
            
        
        case 'color-options':
            hex_list: list[str] = split_str[1].split(',')
            
            for hex in hex_list:
                log(ColorHandler.hex_to_rgb(hex))
            
            
            
            
            
        
        
        case _:
            log('No handler for: ' + split_str[0])

def _on_pc_connection():
    log('Successfully established connection with PC.')
    LEDHandler.cleanup()
    
    global _is_connected
    _is_connected = True
    
    start_thread(maintain_connection)
    DatabaseHandler.close()
    

def _get_device_status() -> str:
    temp: str = str(get_temp())
    wifi_connection: str = 'true' if WifiHandler.is_connected() else 'false'
    
    return 'status {' + f'"temp": {temp}, "wifi": {wifi_connection}' + '}'
    
    

def _attempt_wifi(ssid: str, password: str) -> None:
    log("Attempting wifi connection with " + ssid + " and " + password)
    write('wifi start')
    
    run(['sudo', 'raspi-config', 'nonint', 'do_wifi_ssid_passphrase', ssid, password]) 
    log("Checking wifi connection...")
    write('wifi end')
    

    if WifiHandler.attempt_wifi_connection():
        log("Wifi connected.")
        write('wifi connected')
    else:
        log("Wifi not connected.")
        write('wifi disconnected')


    


def write(data: str, out: bool = True) -> None:
    if _ser != None:
        # if out:
            # log("Sending " + str(data))
            
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
        if _is_connected:
            write('pi_exit')
            time.sleep(0.1)
        _ser.close()
        
    
if __name__ == '__main__':
    try:
        init()
        listen()
    except KeyboardInterrupt:
        cleanup()