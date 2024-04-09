import asyncio
import struct
import threading 
from bleak import BleakClient
import time
from flask import Flask, jsonify
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# Define the UUIDs of the service and characteristic from Arduino
address = "705E0B07-DE6F-A403-C7FE-23C804F8A01A"
SERVICE_UUID = "19B10000-E8F2-537E-4F6C-D104768A1214"
CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database']  # Replace 'your_database' with your database name
collection = db['your_collection']  # Replace 'your_collection' with your collection name


# Initialize lists to store received data
time_data = []
sensor_data = []

async def read_data(address):
    start_time = time.time()
    
    async with BleakClient(address) as client:
        # Wait for the connection to be established
        if not client.is_connected:
            await client.connect()
        print("Connected!")

        # Read the data from the characteristic and plot it
        while time.time() - start_time < 10:
            try:
                value = await client.read_gatt_char(CHARACTERISTIC_UUID)
                # Convert bytes to float (assuming little-endian encoding)
                sensor_val = struct.unpack('<f', value)[0]
                print("Received data:", sensor_val)
                
                # Append data to lists
                time_data.append(len(time_data) + 0.5)  # Append the current time
                sensor_data.append(sensor_val)

            except Exception as e:
                print("Error reading data:", e)

            # Add a delay between readings
            await asyncio.sleep(0.05)

@app.route('/')
def index():
    return "Hello, this is your Flask app!"

@app.route('/data')
def display_data():
    # Return the collected data as JSON
    return {
        "time_data": time_data,
        "sensor_data": sensor_data
    }
    
@app.route('/get_data', methods=['GET'])
def get_data():
    # Retrieve data from MongoDB collection
    cursor = collection.find({}, {'_id': 0})  # Exclude _id field from the results
    data = list(cursor)  # Convert cursor to list

    # Format the data as a pretty list
    pretty_list = [f"{index+1}. {entry}" for index, entry in enumerate(data)]

    return jsonify(pretty_list)
    

    
@app.route('/add_data', methods=['POST'])
def add_data():
    
    data = {
        "time_data": time_data,
        "sensor_data": sensor_data
    }

    if data:
        # Insert document into MongoDB collection
        inserted_data = collection.insert_one(data)
        return jsonify({'message': 'Data added successfully', 'inserted_id': str(inserted_data.inserted_id)})
    else:
        return jsonify({'error': 'No data received'})

if __name__ == "__main__":
    # Replace 'your_device_address' with the actual address of your Arduino BLE peripheral
    device_address = "705E0B07-DE6F-A403-C7FE-23C804F8A01A"

    # Create a new event loop
    loop = asyncio.new_event_loop()

    # Run the event loop until the read_data coroutine completes
    loop.run_until_complete(read_data(device_address))

    # Run Flask app without the reloader
    app.run(debug=True, use_reloader=False)
