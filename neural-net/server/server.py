from flask import Flask
from flask_socketio import SocketIO, send
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# get between 1 and 100 randomly sampled neurons from the network of 625
# activate each neuron in the sample with a random activity level between 0 and 1


def randActivity(neuronsX=25, neuronsY=25):
    neurons = range(neuronsX * neuronsY)
    neuronSample = random.sample(neurons, random.randint(1, 100))
    return [0 if i not in neuronSample else random.uniform(0, 1) for i in neurons]


@app.route('/')
def home():
    return 'Home'


@socketio.on('connect')
def handle_connection():
    print('Client connected!')
    socketio.emit('new-activity', {'hi': 'hey'})
    socketio.emit('new-activity', {
        'sensoryInput': randActivity(),
        'area1': randActivity(),
        'area2': randActivity(),
        'area3': randActivity(),
        'area4': randActivity(),
        'area5': randActivity(),
        'area6': randActivity(),
        'motorInput1': randActivity(),
    })


@socketio.on('disconnext')
def handle_disconnection():
    print('Client disconnected!')


@socketio.on('message')
def handle_message(message):
    print('Message Received: ' + message)
    send(message)


if __name__ == '__main__':
    socketio.run(app, host='localhost', port=9000)
