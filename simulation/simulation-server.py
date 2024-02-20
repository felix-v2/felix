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

active_client_connection = None
model = None
sim_manager: SimulationManager = None


@app.route('/')
def home():
    return 'Home'


"""
Connect

Establishes a connection with the client ready for realtime bidirectional communication between
the gui (sending to the net user-modified parameter values) and the neural net (sending to the gui network activity at each step)
We allow only one client connection at a time here, and assume only a single (local) user who can
disconnect and reconnect to a simulation as it runs server side
"""


@socketio.on('connect')
def handle_connection():
    global active_client_connection
    if active_client_connection is not None:
        # Disconnect the new connection if there is already an active connection
        socketio.emit('disconnect', {'msg': 'Connection already active.'})
        return False

    # Store the session ID of the active connection
    active_client_connection = request.sid

    print(f'Client {request.sid} connected!')
    print(
        f'Simulation {"is" if sim_manager and sim_manager.simulation_running else "is not"} running!')
    print(
        f'Model execution is at step {model.current_step if model else 0}.')


"""
Disconnect

@todo the client should be able to disconnect and then connect again, "resuming" the simulation as they left off
but should we somehow enforce that it is indeed the "same" client (can we?)
I think it's ok - since the toolbox only runs locally and only one client can be connected at a time
"""


@socketio.on('disconnect')
def handle_disconnection():
    global active_client_connection
    active_client_connection = None
    print(f'Client {request.sid} disconnected!')


"""
update-config

Receives new model parameter values from the client and queues them for the model thread to consume
"""


@socketio.on('update-config')
def handle_update_config(new_config):
    print(f'\n\nNew simulation config received: {new_config}')

    if sim_manager:
        if model:
            print(f'\n\Model step: {model.current_step}')

        sim_manager.update_config(new_config)
        print(f'\n\nUpdated model config: {model.config}')


"""
start-simulation

Initialises the model and starts execution in a background thread
"""


@socketio.on('start-simulation')
def handle_start_simulation(initial_config):
    print(f'Start-sim request received from client {request.sid}')

    global model, sim_manager

    # @todo this is actually the same thing under the hood - just starts the background thread
    # so we might be able to just remove it
    # Resume a simulation that's already running, picking up the model state where it left off
    if model and sim_manager:
        print(f'\n\Simulation resuming: {sim_manager.simulation_running}')
        print(f'\n\Model step: {model.current_step}')
        sim_manager.resume_simulation(initial_config)
        return True

    # Initialise a new simulation
    if not model or not sim_manager:
        model = MockNeuralNet()  # StandardNet6Areas()
        sim_manager = SimulationManager(model, socketio)
        sim_manager.start_simulation(initial_config)

        print(f'\n\Simulation running: {sim_manager.simulation_running}')
        print(f'\n\Model step: {model.current_step}')


"""
stop-simulation

Pauses execution of the model (the model state will persist as long as the server is live)
"""


@socketio.on('stop-simulation')
def handle_stop_simulation():
    global sim_manager
    if sim_manager and sim_manager.simulation_running:
        print(f'\n\Model stopping at step: {model.current_step}')
        sim_manager.stop_simulation()
        print(f'\n\Simulation running: {sim_manager.simulation_running}')


"""
resume-simulation

Resume execution of the model
"""


@socketio.on('resume-simulation')
def handle_resume_simulation():
    global sim_manager
    if sim_manager and not sim_manager.simulation_running:
        print(f'\n\Model resuming at step: {model.current_step}')
        sim_manager.resume_simulation()
        print(f'\n\Simulation running: {sim_manager.simulation_running}')


if __name__ == '__main__':
    # Start the WebSocket server
    socketio.run(app, host='localhost', port=9000)
