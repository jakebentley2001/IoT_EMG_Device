import asyncio
import struct
import threading 
from bleak import BleakClient
import time
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# Define the UUIDs of the service and characteristic from Arduino
address = "705E0B07-DE6F-A403-C7FE-23C804F8A01A"
SERVICE_UUID = "19B10000-E8F2-537E-4F6C-D104768A1214"
CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Connect to MongoDB
client = MongoClient('mongodb+srv://jakebentley2001:Sonicpower4@serverlessinstance0.hzqw4sr.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance0')
#ServerlessInstance0
db = client['IOT_DEVICE']  # Replace 'your_database' with your database name
collection = db['muscle_data']  # Replace 'your_collection' with your collection name

record = "2"

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
            
                # Prepare data for insertion
 
    
    data_to_insert = {"record_number": record, "data": [time_data , sensor_data]}

    # Insert collected data into MongoDB collection
    if data_to_insert:
        collection.insert_one(data_to_insert)
        
    #document = collection.find_one({"record_number": record})

    #print(document)  

@app.route('/')
def index():
    #return "Hello, this is your Flask app!"
    return render_template('index.html')


# @app.route('/data')
# def display_data():
    
#     # Filter based on record_number
#     document = collection.find_one({"record_number": record})


#     return jsonify(document["data"])

@app.route('/get_recording_data', methods=['GET'])
def get_recording_data():
    # Retrieve data from database (replace with your logic)
    document = collection.find_one({"record_number": record})
    
    record_number = document["record_number"]
    sensor_data = document['data'][1]
    time_data = document['data'][0]
    
    
    # ...
    return jsonify({"record_number": record_number, "data": sensor_data})


@app.route('/get_recording', methods=['POST'])
def get_recording():
    record_number = request.form.get('record_number')

    # Retrieve data from database (replace with your logic)
    document = collection.find_one({"record_number": record_number})

    if document:
        return render_template('index.html', result=document)
    else:
        return render_template('index.html', error="Record not found!")


if __name__ == "__main__":
    # Replace 'your_device_address' with the actual address of your Arduino BLE peripheral
    device_address = "705E0B07-DE6F-A403-C7FE-23C804F8A01A"

    # Create a new event loop
    loop = asyncio.new_event_loop()

    # Run the event loop until the read_data coroutine completes
    loop.run_until_complete(read_data(device_address))

    # Run Flask app without the reloader
    app.run(debug=True, use_reloader=False)
