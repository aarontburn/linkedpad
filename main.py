from threading import Thread
from time import sleep
import GPIOHandler
import DatabaseHandler
import LEDHandler
import SerialHandler
from log import log
import socket

def init():
    log("Booting...")
    LEDHandler.init()
    GPIOHandler.setup_gpio()
    DatabaseHandler.init_db()

    start_thread(SerialHandler.init)
    start_thread(GPIOHandler.gpio_listen)
    start_thread(DatabaseHandler.db_listen)


    exiting = False
    try:
        while not exiting:
            sleep(0.5)
            # log("Temp: " + str(_get_temp()) + " C")
    except KeyboardInterrupt:
        log("Exiting program...")
        exiting = True
        _run_with_exception(LEDHandler.cleanup)
        _run_with_exception(SerialHandler.cleanup)
        _run_with_exception(DatabaseHandler.close)
        _run_with_exception(GPIOHandler.destroy_gpio)



def _run_with_exception(target) -> None:
    try:
        target()
    except Exception as e:
        log(e)
    


def start_thread(target, args = ()):
    thread = Thread(target=target, args=args)
    thread.daemon = True
    thread.start()


def get_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return round(int(f.read().strip()) / 1000, 2)
    
    
    
if __name__ == '__main__':
    init()




# Pins 4, 6, 12 for LED
# Pins 29, 31, 33, 35, 37 for Key Rows
# Pins 32, 36, 38, 40 for Key Columns

# 32, 29 for H0
