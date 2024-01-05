from flask import Flask, request
from flask_socketio import SocketIO, emit
import random
from threading import Timer

"""initialise websocket server"""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')


"""
get between 1 and 100 randomly sampled neurons from the network of 625
activate each neuron in the sample with a random activity level between 0 and 1
"""


def randActivity(neuronsX=25, neuronsY=25):
    neurons = range(neuronsX * neuronsY)
    sample = random.sample(neurons, random.randint(1, 100))
    matrix = []
    for i in range(neuronsX):
        row = []
        for j in range(neuronsY):
            neuron = (i+1)*(j+1)
            row.append(0 if neuron not in sample else random.uniform(0, 1))
        matrix.append(row)
    return matrix


"""web server handler for root"""


@app.route('/')
def home():
    return 'Home'


def sendActivity():
    emit('new-activity', {
        'sensoryInput1': randActivity(),
        'area1': randActivity(),
        'area2': randActivity(),
        'area3': randActivity(),
        'area4': randActivity(),
        'area5': randActivity(),
        'area6': randActivity(),
        'motorInput1': randActivity(),
    })


"""Handle connection from gui client"""


@socketio.on('connect')
def handle_connection():
    print(f'Client {request.sid} connected!')
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()
    sendActivity()


"""Handle disconnection by gui client"""


@socketio.on('disconnect')
def handle_disconnection():
    print(f'Client {request.sid} disconnected!')


"""Handle message from gui client"""


@socketio.on('message')
def handle_message(message):
    print(f'Message received from client {request.sid}: {message}')


if __name__ == '__main__':
    socketio.run(app, host='localhost', port=9000)
