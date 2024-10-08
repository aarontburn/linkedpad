import pymongo
import ColorHandler
import SerialHandler
from Helper import log, pwd, run_with_exception, start_thread

import WifiHandler
if __name__ != "__main__":
    import LEDHandler

_is_init: bool = False

_URI: str = None
_client = None
_database = None
_collection = None
_stream = None


_ACCESS_QUERY: dict[str, str] = {'accessID': ':3'}

_KEYS: list[str] = [row + col for row in ["A", "B", "C", "D"] for col in ["0", "1", "2", "3"]]



def _get_default_obj() -> dict:
    o = {}
    for key in _KEYS:
        o[key] = ColorHandler.OFF
    key = list(_ACCESS_QUERY.keys())[0]
    o[key] = _ACCESS_QUERY[key]
    return o


_DEFAULT_DB_OBJ: dict = _get_default_obj()

_local_state: dict[str, str] = {}

def init() -> None:
    WifiHandler.add_listener(_wifi_listener)

    
    with open(pwd() + '/key.txt', 'r') as f:
        username_password: list[str] = f.read().replace("\n", '').split(" ")
        
        global _URI
        _URI = f"mongodb+srv://{username_password[0]}:{username_password[1]}@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad"





def _wifi_listener(is_connected: bool) -> None:
    if is_connected:
        if SerialHandler.is_connected() == False:
            init_db()
            
    else: # Disconnect
        if SerialHandler.is_connected() == False:
            close()
            
            
            
            
        
        
        
        

def init_db() -> None:
    log("Initializing...")
    
    ColorHandler.load_colors_from_storage()
    
    global _client
    global _database
    global _collection
    
    _client = pymongo.MongoClient(_URI)
    _database = _client.get_database('pad_data')
    _collection = _database.get_collection('data')
    
    LEDHandler.set_light('H3', ColorHandler.WHITE)
    
    _check_database()
    _collection.find_one({})
    recalibrate()
    LEDHandler.set_light('H3', ColorHandler.OFF)
    
    
    global _is_init
    _is_init = True
    LEDHandler.set_light('H0', ColorHandler.get_current_color())
    log("Finished initializing.")


def db_listen() -> None:
    if _is_init == False:
        return
    
    log("Database listener started.")
    
    global _stream
    _stream = _collection.watch()
    try:
        with _stream:
            for change in _stream:
                _on_database_change(change['updateDescription']['updatedFields'])
    except Exception as e:
        close()


def on_key_press(row_col: str) -> None:
    is_off: bool = _local_state[row_col] == ColorHandler.OFF
    _collection.find_one_and_update(_ACCESS_QUERY, {"$set": {row_col: ColorHandler.get_current_color() if is_off else ColorHandler.OFF}})


def close() -> None:
    log('Closing...')
    global _is_init
    _is_init = False
    
    
    if _stream != None:
        run_with_exception(_stream._cursor.close)
    
    if _client != None:
        run_with_exception(_client.close)
    

def reset() -> None:
    _collection.find_one_and_update(
        _ACCESS_QUERY,
        {'$set': _DEFAULT_DB_OBJ},
        return_document=pymongo.ReturnDocument.AFTER, upsert=True,
    )
    
    recalibrate()


def recalibrate() -> None:
    current_state: dict[str, str] | None = _get_object()
    if current_state == None:
        log("Could not recalibrate; '_get_object()' returned 'None'")
        return
    
    for key in _KEYS:
        _set_light(key[0], key[1], ColorHandler.OFF);
    
    for key in _KEYS:
        _set_light(key[0], key[1], current_state[key])


def _check_database() -> None:
    if _collection.estimated_document_count() == 1:
        entry: dict[str, str] | None = _get_object()
        if entry is not None:
            if sorted(entry.keys()) == sorted(_KEYS + ['_id', 'accessID']):
                log("Database is properly initialized.")
                return
    log("WARNING: Database needs to be re-setup.")
    _collection.delete_many({})
    reset()


    
def _on_database_change(change_object: dict[str, str]) -> None:
    if SerialHandler.is_connected():
        return 
    
    for row_col in change_object:
        row: str = row_col[0]
        col: str = row_col[1]
        new_value: list[int, int, int] = change_object[row_col]
        _set_light(row, col, new_value)


def _set_light(row: str, col: str, state: list[int, int, int]) -> None:
    _local_state[row + col] = state
    # _display_to_console()
    if __name__ != "__main__":
        LEDHandler.set_light(row + col, state)
    


def _get_object() -> dict[str, str] | None:
    return _collection.find_one(_ACCESS_QUERY)


def _display_to_console() -> None:
    s: str = ''
    for i in range(len(_KEYS)):
        if i % 4 == 0:
            s += "\n"
        try:
            t: list[int, int, int] = _local_state[_KEYS[i]]
            s += str(ColorHandler.rgb_to_hex(t)) + " "
        except KeyError:
            s += '#ZZZZZZ '
    log(s)
    






if __name__ == "__main__":
    try:
        init_db()
        db_listen()
    except KeyboardInterrupt:
        close()
        