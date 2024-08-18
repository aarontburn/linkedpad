import serial
from log import log
import time
import asyncio
from threading import Thread
from main import _start_thread

_PORT: str = '/dev/ttyGS0'
_BAUD: int = 9600

_ser: serial.Serial = None

def init():
    _establish_serial()
    _attempt_connection()
    listen()

def _attempt_connection() -> None: 
    log('Attempting to connect to PC...')
    
    while True:
        write('pi_ready')
        time.sleep(1)
        
        data: str = str(_ser.readline())[2:-3];
        if (data != '') {
            print(data)
        }
        if data == 'pc_ready':
            return
        


def listen() -> None:
    log("Listening...")
    while True:
        try:
            data: str = str(_ser.readline())[2:-3]
            
            if data != '':
                log("Received: " + data)
        except Exception:
            _establish_serial()


def write(data: str) -> None:
    if _ser != None:
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