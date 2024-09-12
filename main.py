from time import sleep
import ColorHandler
import GPIOHandler
import DatabaseHandler
import LEDHandler
import SerialHandler
import WifiHandler
from Helper import start_thread, log, run_with_exception


def init():
    log("Booting...")
    LEDHandler.init()
    GPIOHandler.setup_gpio()
    DatabaseHandler.init()
    
    start_thread(SerialHandler.init)
    
    # Do loading animation
    _await_boot_finish()
    WifiHandler.listen_to_wifi()
    
    
    if (SerialHandler.is_connected() == False):
        DatabaseHandler.init_db()
        
    
    
    sleep(0.25)

    start_thread(GPIOHandler.gpio_listen)
    start_thread(DatabaseHandler.db_listen)


    exiting = False
    try:
        while not exiting:
            sleep(0.5)
            # log("Temp: " + str(_get_temp()) + " C")
    except KeyboardInterrupt:
        exiting = True
        _on_exit()



def _await_boot_finish() -> None:
    log("Starting boot")
    
    log("\tAwaiting Wifi or PC connection...")
    
    LEDHandler.set_light('H3', ColorHandler.WHITE)
    
    MAX_POLLING_SECS: int = 15
    
    i: int = 0
    while True:
        log('\t\tCONNECTION ATTEMPT #' + str(i))
        if WifiHandler.attempt_wifi_connection():
            log("\tWifi connection found.")
            break
        
        if SerialHandler.is_connected():
            log("\tConnected to PC.")
            break
        
        i += 1
        if i == MAX_POLLING_SECS:
            log(f"\tNo connections found after {MAX_POLLING_SECS} seconds.")
            LEDHandler.set_light('H3', ColorHandler.RED)
            
        sleep(1)
        
    LEDHandler.cleanup()
    log("\tBoot processed finished.")
    
    
    


    
def _on_exit():
    log("Exiting program...")
    run_with_exception(LEDHandler.cleanup)
    run_with_exception(SerialHandler.cleanup)
    run_with_exception(DatabaseHandler.close)
    run_with_exception(GPIOHandler.destroy_gpio)
    
    
if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        _on_exit()




# Pins 4, 6, 12 for LED
# Pins 29, 31, 33, 35, 37 for Key Rows
# Pins 32, 36, 38, 40 for Key Columns

# 32, 29 for H0
