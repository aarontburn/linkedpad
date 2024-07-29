import pymongo

# MongoDB setup
URI = "mongodb+srv://admin:j2MzVYcewmPjnzrG@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad"
ACCESS_QUERY = {'accessID': ':3'}

def __get_keys__():
    rows = ["A", "B", "C", "D"]
    columns = ["0", "1", "2", "3"]
    out = []
    for row in rows:
        for col in columns:
            out.append(row + col)
    return out

KEYS = __get_keys__()

def __get_default_obj__():
    o = {}
    for key in KEYS:
        o[key] = 0
    key = list(ACCESS_QUERY.keys())[0]
    o[key] = ACCESS_QUERY[key]
    return o

DEFAULT_DB_OBJ = __get_default_obj__()
local_state = {}

client = pymongo.MongoClient(URI)
database = client.get_database('pad_data')
collection = database.get_collection('data')

def init_mongo():
    print("Initializing database handler...")
    __check_database__()
    collection.find_one({})
    recalibrate()
    
    print("Database initialization finished.")
    

def __check_database__():
    if collection.estimated_document_count() == 1:
        entry = __get_object__()
        if entry is not None:
            if sorted(entry.keys()) == sorted(KEYS + ['_id', 'accessID']):
                print("Database is properly initialized.")
                return
    print("WARNING: Database needs to be re-setup.")
    collection.delete_many({})
    reset()

def listen():
    print("Database listener started.")
    try:
        with collection.watch() as stream:
            for change in stream:
                __on_database_change__(change['updateDescription']['updatedFields'])
    except pymongo.errors.PyMongoError as e:
        client.close()



def on_key_press(row, col):
    collection.find_one_and_update(ACCESS_QUERY, { "$bit": { row + col: { 'xor': 1 } } })
    
    
def close():
    client.close()


def reset():
    result = collection.find_one_and_update(
        ACCESS_QUERY,
        {'$set': DEFAULT_DB_OBJ},
        return_document='after', upsert=True,
    )
    for key in result:
        __set_light__(key[0], key[1], 0)


def recalibrate():
    current_state = __get_object__()
    for key in KEYS:
        __set_light__(key[0], key[1], current_state[key])


def __on_database_change__(change_object):
    for row_col in change_object:
        row = row_col[0]
        col = row_col[1]
        new_value = change_object[row_col]
        __set_light__(row, col, new_value)


def __set_light__(row, col, isOn):
    local_state[row + col] = isOn
    __displayStateToConsole__()

def __get_object__():
    return collection.find_one(ACCESS_QUERY)

def __displayStateToConsole__():
    s = ''
    for i in range(len(KEYS)):
        if i % 4 == 0:
            s += "\n"
        try:
            t = local_state[KEYS[i]]
            s += '1 ' if t > 0 else '0 '
        except KeyError:
            s += '0 '
    print(s)
    
