import { MongoClient } from "mongodb";

import { SerialPort } from 'serialport'

// Create a port
const port = new SerialPort({
    path: '/dev/tty0',
    baudRate: 115200,
})

// Switches the port into "flowing mode"
port.on('data', function (data) {
    console.log('Data:', data)
})




const ACCESS_QUERY = { 'accessID': ':3' }

// ["A1", "A2", ..., "D4"]
const KEYS = (() => {
    const rows = ["A", "B", "C", "D"];
    const columns = ["0", "1", "2", "3"];

    const out = [];

    for (let i = 0; i < rows.length; i++) {
        for (let j = 0; j < columns.length; j++) {
            out.push(rows[i] + columns[j]);
        }
    }
    return out;
})();

// { "A0": 0, "A1": 0, ..., "D4": 0, "accessID": ":3" }
const DEFAULT_DB_OBJ = (() => {
    const object = {};
    for (const key of KEYS) {
        object[key] = 0;
    }
    const key = Object.keys(ACCESS_QUERY)[0];
    object[key] = ACCESS_QUERY[key];
    return object;
})();

const localState = {};

const URI = "mongodb+srv://admin:j2MzVYcewmPjnzrG@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad";


const client = new MongoClient(URI);
const database = client.db("pad_data");
const collection = database.collection("data");



async function initialize() {
    console.log("Initializing...");

    checkDatabase().then(() => {
        collection.findOne({}).then(async data => {
            await recalibrate();
            listen().catch(initialize); // Reboot if error
        });
    });
}

async function checkDatabase() {
    if (await collection.estimatedDocumentCount() === 1) {
        const entry = await getObject();

        if (entry !== null) {
            if (Object.keys(entry).sort().toString() === [...KEYS, '_id', 'accessID'].sort().toString()) { // All keys are valid
                console.log("Database is properly initialized.");
                return;
            }
        }
    }

    console.log("WARNING: Database needs to be re-setup.");
    await collection.deleteMany({});
    await reset();
}

/**
 *  Listens to any database changes.
 */
async function listen() {
    try {
        const changeStream = collection.watch();
        console.log("Listening for changes...");

        // Print change events as they occur
        for await (const change of changeStream) {
            if (change && change.updateDescription && change.updateDescription.updatedFields) {
                onDatabaseChange(change.updateDescription.updatedFields)
            }
        }
        await changeStream.close();

    } finally {
        await client.close();
    }
}


/**
 *  An event that triggers when the database object is modified.
 *  @param changeObject     An object containing all keys and new states for each button.
 */
function onDatabaseChange(changeObject) {
    for (const rowCol in changeObject) {
        if (!KEYS.includes(rowCol)) { // Maybe not needed?
            continue;
        }

        const row = rowCol[0];
        const col = rowCol[1];
        const newValue = changeObject[rowCol];
        setLight(row, col, newValue);
    }
}

/**
 *  Reset all buttons to 0
 */
async function reset() {
    const result = await collection.findOneAndUpdate(
        ACCESS_QUERY,
        { '$set': DEFAULT_DB_OBJ }, { returnDocument: 'after', upsert: true });

    for (const key in result) {
        setLight(key[0], key[1], 0);
    }
}

/**
 *  Recalibrates all lights to the state reflected in the database.
 */
async function recalibrate() {
    const currentState = await getObject();

    for (const key of KEYS) {
        setLight(key[0], key[1], currentState[key]);
    }
}


async function getObject() {
    return await collection.findOne(ACCESS_QUERY);
}


function setLight(row, col, isOn) {
    localState[row + col] = isOn;
    displayStateToConsole();
    // TODO: Implement the actual light toggle
}


// Flips whatever the button position is.
async function onClick(row, col) {
    await collection.findOneAndUpdate(
        ACCESS_QUERY,
        { "$bit": { [row + col]: { 'xor': 1 } } }
    )
}

function displayStateToConsole() {
    let s = '';

    for (let i = 0; i < KEYS.length; i++) {
        if (i % 4 === 0) {
            s += "\n";
        }

        const t = localState[KEYS[i]];

        if (t === undefined) {
            s += '0 ';
        } else {
            s += t > 0 ? '1 ' : '0 ';
        }
    }

    console.log(s);
}

initialize();