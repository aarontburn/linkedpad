import pymongo

_URI = "mongodb+srv://admin:j2MzVYcewmPjnzrG@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad"
_CLIENT = pymongo.MongoClient(_URI)
_DATABASE = _CLIENT.get_database('pad_data')
_COLLECTION = _DATABASE.get_collection('data')


_ACCESS_QUERY = {'accessID': ':3'}

_KEYS = [row + col for row in ["A", "B", "C", "D"] for col in ["0", "1", "2", "3"]]

def _get_default_obj():
    o = {}
    for key in _KEYS:
        o[key] = 0
    key = list(_ACCESS_QUERY.keys())[0]
    o[key] = _ACCESS_QUERY[key]
    return o

_DEFAULT_DB_OBJ = _get_default_obj()



_local_state = {}



def init_db():
    print("Initializing database handler...")
    _check_database()
    _COLLECTION.find_one({})
    recalibrate()
    
    print("Database initialization finished.")
    



def db_listen() -> None:
    print("Database listener started.")
    try:
        with _COLLECTION.watch() as stream:
            for change in stream:
                _on_database_change(change['updateDescription']['updatedFields'])
    except pymongo.errors.PyMongoError as e:
        _CLIENT.close()



def on_key_press(row, col) -> None:
    _COLLECTION.find_one_and_update(_ACCESS_QUERY, { "$bit": { row + col: { 'xor': 1 } } })
    
    
def close() -> None:
    _CLIENT.close()


def reset() -> None:
    result = _COLLECTION.find_one_and_update(
        _ACCESS_QUERY,
        {'$set': _DEFAULT_DB_OBJ},
        return_document='after', upsert=True,
    )
    for key in result:
        _set_light(key[0], key[1], 0)


def recalibrate() -> None:
    current_state = _get_object()
    for key in _KEYS:
        _set_light(key[0], key[1], current_state[key])

def _check_database() -> None:
    if _COLLECTION.estimated_document_count() == 1:
        entry = _get_object()
        if entry is not None:
            if sorted(entry.keys()) == sorted(_KEYS + ['_id', 'accessID']):
                print("Database is properly initialized.")
                return
    print("WARNING: Database needs to be re-setup.")
    _COLLECTION.delete_many({})
    reset()


def _on_database_change(change_object) -> None:
    for row_col in change_object:
        row = row_col[0]
        col = row_col[1]
        new_value = change_object[row_col]
        _set_light(row, col, new_value)


def _set_light(row, col, isOn) -> None:
    _local_state[row + col] = isOn
    _displayStateToConsole()

def _get_object() -> dict[str, str] | None:
    return _COLLECTION.find_one(_ACCESS_QUERY)

def _displayStateToConsole() -> None:
    s = ''
    for i in range(len(_KEYS)):
        if i % 4 == 0:
            s += "\n"
        try:
            t = _local_state[_KEYS[i]]
            s += '1 ' if t > 0 else '0 '
        except KeyError:
            s += '0 '
    print(s)
    
