import asyncio
import struct
import threading 
from bleak import BleakClient
import time
from flask import Flask, jsonify
from pymongo import MongoClient

# client = MongoClient('mongodb://jakebentley2001:Sonicpower4@serverlessinstance0.hzqw4sr.mongodb.net/')
# #ServerlessInstance0
# db = client['IOT_DEVICE']  # Replace 'your_database' with your database name
# collection = db['muscle_data']  # Replace 'your_collection' with your collection name

# time_data = [0,1,2,3]
# sensor_data = [1,4,5,9]
# data_to_insert = [{"time_data": time_data[i], "sensor_data": sensor_data[i]} for i in range(len(time_data))]

# collection.insert_many(data_to_insert)
import ssl
print(ssl.OPENSSL_VERSION)
