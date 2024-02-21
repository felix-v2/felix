import random
from flask_socketio import SocketIO, emit
from flask import Flask, request
import eventlet
# https://stackoverflow.com/questions/34581255/python-flask-socketio-send-message-from-thread-not-always-working
eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')


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


@app.route('/')
def home():
    return 'Home'


@socketio.on('connect')
def handle_connection():
    print(f'Client {request.sid} connected!')


@socketio.on('disconnect')
def handle_disconnection():
    print(f'Client {request.sid} disconnected!')


@socketio.on('start-simulation')
def handle_start_simulation(initial_config):
    print(f'Start-sim request received from client {request.sid}')
    while True:
        socketio.sleep(1)
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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
