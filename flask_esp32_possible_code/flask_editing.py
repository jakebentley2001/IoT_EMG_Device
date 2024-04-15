from flask import Flask, render_template
from flask_socketio import SocketIO
#import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*",path = '/socket.io')

#cors_allowed_origins=["http://192.168.0.184:3000", "file://", "ws://192.168.0.100:3000/socket.io/?EIO=4"]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
       
@socketio.on('my_event')
def handle_message(message):
    print('Received message from client:', message)

@socketio.on('Button value changed')
def handle_button_value(data):
    print('Button value changed:', data)
    # Handle the received button value here
    # For demonstration purposes, let's broadcast the received value to all clients
    socketio.emit('update value', data)
    
@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)