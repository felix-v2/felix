import random
from queue import Queue
import time
import threading
from flask_socketio import SocketIO
from flask import Flask, request
import eventlet
# https://stackoverflow.com/questions/34581255/python-flask-socketio-send-message-from-thread-not-always-working
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')


class Simulator:
    def __init__(self, initial_config):
        # fixed model params
        self.steps = 100
        self.areas = 6
        self.neuronsX = 25
        self.neuronsY = 25

        # for non-blocking simulation runs, with dynamic in-simulation config updates
        self.config_queue = Queue()
        self.simulation_lock = threading.Lock()
        self.simulation_running = False

        # the current version of the simulation parameters
        self.config = initial_config

        # current network activity
        # sensoryInput, area1, area2, area3, area4, area5, area6, motorInput = self.silence()

    def silence(self):
        w, h = self.neuronsX, self.neuronsY
        return [[0 for x in range(w)] for y in range(h)]

    def randomActivity(self):
        neurons = range(self.neuronsX * self.neuronsY)
        sample = random.sample(neurons, random.randint(1, 100))
        matrix = []
        for i in range(self.neuronsX):
            row = []
            for j in range(self.neuronsY):
                neuron = (i+1)*(j+1)
                row.append(0 if neuron not in sample else random.uniform(0, 1))
            matrix.append(row)
        return matrix

    def mockNetworkActivity(self):
        return {
            'sensoryInput1': self.silence() if self.config.get('applySensoryInput') is False else self.randomActivity(),
            'area1': self.randomActivity(),
            'area2': self.randomActivity(),
            'area3': self.randomActivity(),
            'area4': self.randomActivity(),
            'area5': self.randomActivity(),
            'area6': self.randomActivity(),
            'motorInput1': self.silence() if self.config.get('applyMotorInput') is False else self.randomActivity(),
        }

    # TODO move threading into socketio handlers
    # start simulation loop in background thread
    def start_simulation(self):
        with self.simulation_lock:
            if not self.simulation_running:
                self.simulation_running = True
                simulation_thread = threading.Thread(
                    target=self.simulation_loop)
                simulation_thread.start()

    def update_config(self, new_config):
        self.config_queue.put(new_config)

    def simulation_loop(self):
        for step in range(self.steps):
            # Check for updated config from the main thread
            if not self.config_queue.empty():
                new_config = self.config_queue.get()
                self.config.update(new_config)

            print(
                f'\n\nSim step {step + 1} config: {self.config}')

            # Perform simulation computation using simulation_config
            activity = self.mockNetworkActivity()

            # Logging for demo purposes
            motorInput = activity.get('sensoryInput1')
            sensInput = activity.get('motorInput1')
            print(f'Sim step {step + 1} sensory input rows: {len(sensInput)}')
            print(f'Sim step {step + 1} motor input rows: {len(motorInput)}')

            # Send the result_data to the client
            # TODO rename to "simulation_step_activity"
            socketio.emit('new-activity', activity)

            # Sleep to simulate a delay between steps
            time.sleep(0.5)

            if not self.simulation_running:
                break


@app.route('/')
def home():
    return 'Home'


simulator = None


@socketio.on('connect')
def handle_connection():
    print(f'Client {request.sid} connected!')


# TODO stop simulation and kill thread
@socketio.on('disconnect')
def handle_disconnection():
    print(f'Client {request.sid} disconnected!')


@socketio.on('update-config')
def handle_update_config(new_config):
    print(f'\n\nNew simulation config received: {new_config}')

    if simulator:
        simulator.update_config(new_config)


@socketio.on('start-simulation')
def handle_start_simulation(initial_config):
    print(f'Start-sim request received from client {request.sid}')
    global simulator
    if not simulator:
        simulator = Simulator(initial_config)
        simulator.start_simulation()


if __name__ == '__main__':
    # Start the WebSocket server
    socketio.run(app, host='localhost', port=9000)
