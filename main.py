from threading import Thread
import time
import GPIOHandler
import DatabaseHandler
import LEDHandler
import SerialHandler
from log import log

def init():
    
    log("Booting...")
    LEDHandler.init()
    GPIOHandler.setup_gpio()
    DatabaseHandler.init_db()

    _start_thread(SerialHandler.init)
    _start_thread(GPIOHandler.gpio_listen)
    _start_thread(DatabaseHandler.db_listen)

    try:
        while True:
            time.sleep(1)
            # log("Temp: " + str(_get_temp()) + " C")
    except KeyboardInterrupt:
        log("Exiting program...")
        try:
            LEDHandler.cleanup()
            SerialHandler.cleanup()
            DatabaseHandler.close()
            GPIOHandler.destroy_gpio()

        except Exception:
            log("Error on close")


def _start_thread(target, args = ()):
    thread = Thread(target=target, args=args)
    thread.daemon = True
    thread.start()


def _get_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return round(int(f.read().strip()) / 1000, 2)
    
    

    
    
if __name__ == '__main__':
    
    init()




# Pins 4, 6, 12 for LED
# Pins 31, 33, 35, 37 for Key Rows
# Pins 32, 36, 38, 40 for Key Columns