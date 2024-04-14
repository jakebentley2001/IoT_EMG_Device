import asyncio
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
from bleak import BleakClient
import time

def run_python_script():
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
                

    # Replace 'your_device_address' with the actual address of your Arduino BLE peripheral
    device_address = "705E0B07-DE6F-A403-C7FE-23C804F8A01A"

    loop = asyncio.new_event_loop()
    loop.run_until_complete(read_data(device_address))
