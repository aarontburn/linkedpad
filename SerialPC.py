# This file will become obsolete once the main program is written in nodejs
import time
import serial
from threading import Thread


_PORT: str = 'COM3'
_BAUD: int = 9600


_ser: serial.Serial = None

def init():
    global _ser
    _ser = serial.Serial(
        _PORT, 
        _BAUD,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.25,
        rtscts=True
    )
    
    
def listen() -> None:
    print("Listening...")
    while True:
        data: str = str(_ser.readline())[2:-1]
        if data != '':
            print("Received: " + data)   


def send(data: str) -> None:
    _ser.write((str(data) + "\n").encode())


def _start_thread(target):
    thread = Thread(target=target)
    thread.daemon = True
    thread.start()

def test():
    counter = 0
    while True:
        time.sleep(1)
        send(counter)

if __name__ == '__main__':
    try:
        init()
        _start_thread(listen)
        test()
        
        
        
        
    except KeyboardInterrupt:
        _ser.close()
        
        
