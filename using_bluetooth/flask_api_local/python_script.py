import asyncio
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
from pymongo import MongoClient
from bleak import BleakClient
import time

def run_python_script():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://jakebentley2001:Sonicpower4@serverlessinstance0.hzqw4sr.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance0')
    db = client['IOT_DEVICE']
    collection = db['muscle_data']
    record = "33"
    #muscle = muscle
    

    CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

    time_data = []
    sensor_data = []

    async def read_data(address):
        start_time = time.time()
        
        async with BleakClient(address) as client:
            if not client.is_connected:
                await client.connect()
            print("Connected!")

            while time.time() - start_time < 10:
                try:
                    value = await client.read_gatt_char(CHARACTERISTIC_UUID)
                    sensor_val = struct.unpack('<f', value)[0]
                    print("Received data:", sensor_val)
                    
                    time_data.append(len(time_data) + 0.5)
                    sensor_data.append(sensor_val)

                except Exception as e:
                    print("Error reading data:", e)

                await asyncio.sleep(0.05)
                
        data_to_insert = {"record_number": record, "data": [time_data, sensor_data]}
        if data_to_insert:
            collection.insert_one(data_to_insert)
                
                

    # Replace 'your_device_address' with the actual address of your Arduino BLE peripheral
    device_address = "705E0B07-DE6F-A403-C7FE-23C804F8A01A"

    loop = asyncio.new_event_loop()
    loop.run_until_complete(read_data(device_address))
    
    return record
