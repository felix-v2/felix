from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def home():
    return 'Home'


@socketio.on('connect')
def handle_connection():
    print('Client connected!')


@socketio.on('disconnext')
def handle_disconnection():
    print('Client disconnected!')


@socketio.on('message')
def handle_message(message):
    print('Message Received: ' + message)
    send(message)


if __name__ == '__main__':
    socketio.run(app, host='localhost', port=8080)
