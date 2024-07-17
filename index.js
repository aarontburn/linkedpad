// Watch for changes in a collection by using a change stream
import { MongoClient, ObjectId } from "mongodb";
// Replace the uri string with your MongoDB deployment's connection string.
const uri = "mongodb+srv://admin:j2MzVYcewmPjnzrG@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad";


console.log("Listening for changes:")
const client = new MongoClient(uri);
// Declare a variable to hold the change stream
let changeStream;
// Define an asynchronous function to manage the change stream
async function run() {
  try {
    const database = client.db("pad_data");
    const data = database.collection("data");


    data.findOne(new ObjectId('669724e26784a639c2fdaed0')).then(data => {
        console.log(data)
    });


    changeStream = data.watch();
    // Print change events as they occur
    for await (const change of changeStream) {
        console.log(change.updateDescription.updatedFields)
    }
    // Close the change stream when done
    await changeStream.close();
    
  } finally {
    await client.close();
  }
}
run().catch(console.dir);