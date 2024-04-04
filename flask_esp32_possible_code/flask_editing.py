#This installed version Werkzeug 2.0.0
# Flask 2.3.3 Flask-SocketIO 4.3.1
# python-engineio 3.13.2 python-socketio 4.6.0
from flask import Flask, render_template, Request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

connected_clients = set()

@socketio.on('connect')
def handle_connect():
    sid = socketio.sid
    connected_clients.add(sid)
    print("Client connected:", sid)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    connected_clients.remove(sid)
    print("Client disconnected:", sid)

@socketio.on('123')
def handle_message(message):
    print("Received message from client:", message)
    # Broadcast the received message to all connected clients
    for client in connected_clients:
        emit('123', message, room=client)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
