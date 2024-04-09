import asyncio
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
from bleak import BleakClient

# Define the UUIDs of the service and characteristic from Arduino
address = "705E0B07-DE6F-A403-C7FE-23C804F8A01A"
SERVICE_UUID = "19B10000-E8F2-537E-4F6C-D104768A1214"
CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Initialize lists to store received data
time_data = []
sensor_data = []

# Define a function to update the plot
def update_plot(i):
    plt.cla()
    plt.plot(time_data, sensor_data)
    plt.xlabel('Time')
    plt.ylabel('Sensor Data')

async def read_data(address, loop):
    async with BleakClient(address, loop=loop) as client:
        # Wait for the connection to be established
        if not client.is_connected:
            await client.connect()
        print("Connected!")

        # Read the data from the characteristic and plot it
        while True:
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

if __name__ == "__main__":
    # Replace 'your_device_address' with the actual address of your Arduino BLE peripheral
    device_address = "705E0B07-DE6F-A403-C7FE-23C804F8A01A"

    # Create a new event loop
    loop = asyncio.new_event_loop()

    # Start the event loop in a separate thread
    thread = threading.Thread(target=loop.run_until_complete, args=(read_data(device_address, loop),))
    thread.start()

    # Set up the plot animation
    ani = animation.FuncAnimation(plt.gcf(), update_plot, interval=50)

    # Display the matplotlib figure
    plt.tight_layout()
    plt.show()
