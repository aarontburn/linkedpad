import GPIOHandler
import DatabaseHandler
import threading
import time


def start_gpio_thread():
    gpio_thread = threading.Thread(target=GPIOHandler.gpio_loop)
    gpio_thread.daemon = True
    gpio_thread.start()

def start_mongo_thread():
    mongo_thread = threading.Thread(target=DatabaseHandler.listen)
    mongo_thread.daemon = True
    mongo_thread.start()

if __name__ == '__main__':
    GPIOHandler.setup_gpio()
    DatabaseHandler.init_mongo()
    
    start_gpio_thread()
    start_mongo_thread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIOHandler.destroy_gpio()
        DatabaseHandler.close()