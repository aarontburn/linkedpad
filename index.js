import { MongoClient, ObjectId } from "mongodb";

const KEYS = (() => { // ["A1", "A2", ..., "D4"]
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

const ACCESS_ID = ':3';
const URI = "mongodb+srv://admin:j2MzVYcewmPjnzrG@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad";


const client = new MongoClient(URI);
const database = client.db("pad_data");
const collection = database.collection("data");


async function initialize() {
    console.log("Initializing...");
    await checkDatabase();

    collection.findOne(new ObjectId('669724e26784a639c2fdaed0')).then(async data => {
        listen().catch(console.dir);
    });
}


const VALID_KEYS = [...KEYS, '_id', 'accessID'];

async function checkDatabase() {
    if (await collection.estimatedDocumentCount() === 1) {
        const entry = await getObject();

        if (entry !== null) {
            if (Object.keys(entry).sort().toString() === VALID_KEYS.sort().toString()) { // All keys are valid
                console.log("Database is properly initialized.");
                return;
            }
        }

    }

    console.log("WARNING: Database needs to be re-setup.");
    await collection.deleteMany({});
    await reset();
}

async function listen() {
    let changeStream;
    try {
        changeStream = collection.watch();
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

async function onDatabaseChange(changeObject) {
    const row = Object.keys(changeObject);
    const unparsedData = changeObject[row];
    console.log(row);
    console.log(changeObject[row]);

    for (let i = 0; i < unparsedData.length; i++) {
        if (unparsedData > 0) {
            // Turn light on

            continue;
        }
        // Turn light off
    }
}



async function reset() {
    // Iterate over A0, A1, ... D3, D4 and reset their entries to 0
    const object = {};
    for (const key of KEYS) {
        object[key] = 0;
    }
    object['accessID'] = ACCESS_ID;
    await insertObjectIntoDatabase(object);
}

async function insertObjectIntoDatabase(object) {
    await collection.replaceOne({ 'accessID': ACCESS_ID }, object, { upsert: true });
}

async function getObject() {
    return await collection.findOne({ 'accessID': ACCESS_ID });
}

// async function updateDatabase(row, )

initialize();