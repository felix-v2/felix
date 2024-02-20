from model import MockNeuralNet
from simulation_manager import SimulationManager
from flask_socketio import SocketIO
from flask import Flask, request
import eventlet
# https://stackoverflow.com/questions/34581255/python-flask-socketio-send-message-from-thread-not-always-working
eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')

model = None
sim_manager = None


@app.route('/')
def home():
    return 'Home'


@socketio.on('connect')
def handle_connection():
    print(f'Client {request.sid} connected!')


# @todo stop simulation and kill thread?
@socketio.on('disconnect')
def handle_disconnection():
    print(f'Client {request.sid} disconnected!')


@socketio.on('update-config')
def handle_update_config(new_config):
    print(f'\n\nNew simulation config received: {new_config}')
    print(f'\n\Model step: {model.current_step}')

    if sim_manager:
        sim_manager.update_config(new_config)
        print(f'\n\nUpdated model config: {model.config}')


@socketio.on('start-simulation')
def handle_start_simulation(initial_config):
    print(f'Start-sim request received from client {request.sid}')

    global model, sim_manager
    if not model:
        model = MockNeuralNet()
        sim_manager = SimulationManager(model, socketio)
        sim_manager.start_simulation()
        print(f'\n\Simulation running: {sim_manager.simulation_running}')
        print(f'\n\Model step: {model.current_step}')


@socketio.on('stop-simulation')
def handle_stop_simulation():
    global sim_manager
    if sim_manager and sim_manager.simulation_running:
        print(f'\n\Model stopping at step: {model.current_step}')
        sim_manager.stop_simulation()
        print(f'\n\Simulation running: {sim_manager.simulation_running}')


if __name__ == '__main__':
    # Start the WebSocket server
    socketio.run(app, host='localhost', port=9000)
