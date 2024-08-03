from threading import Thread
import time
import GPIOHandler
import DatabaseHandler
import LEDHandler

def init():
    print("Booting...")
    LEDHandler.init()
    GPIOHandler.setup_gpio()
    DatabaseHandler.init_db()

    _start_thread(GPIOHandler.gpio_listen)
    _start_thread(DatabaseHandler.db_listen)

    try:
        while True:
            time.sleep(1)
            print("Temp: " + str(_get_temp()) + " C")
    except KeyboardInterrupt:
        GPIOHandler.destroy_gpio()
        DatabaseHandler.close()
        LEDHandler.cleanup()


def _start_thread(target):
    thread = Thread(target=target)
    thread.daemon = True
    thread.start()


def _get_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return f.read().strip()


if __name__ == '__main__':
    init()




# Pins 4, 6, 12 for LED
# Pins 31, 33, 35, 37 for Key Rows
# Pins 32, 36, 38, 40 for Key Columns