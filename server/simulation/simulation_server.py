import logging
import json
from .simulation_manager import SimulationManager
from flask_socketio import SocketIO
from flask import Flask, request
import eventlet

# https://stackoverflow.com/questions/34581255/python-flask-socketio-send-message-from-thread-not-always-working
eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger('simulation-server')
logger.setLevel(logging.DEBUG)


@app.route('/')
def home():
    """
    Boilerplate
    """
    return 'Home'


active_client_connection = None
sim_manager: SimulationManager = None


@socketio.on('connect')
def handle_connection():
    """
    Connect

    Establishes a connection with the client ready for realtime bidirectional communication between
    the gui (sending to the net user-modified parameter values) and the neural net (sending to the gui network activity at each step)
    We allow only one client connection at a time here, and assume only a single (local) user who can
    disconnect and reconnect to a simulation as it runs server side
    """
    global active_client_connection
    logger.info(json.dumps({
        'socket-event': 'connect',
        'new client id': request.sid,
    }, sort_keys=False, indent=4))

    if active_client_connection is not None:
        logger.info(json.dumps({
            'socket-event': 'connect',
            'requester client id': request.sid,
            'active client id': active_client_connection,
        }, sort_keys=False, indent=4))

        # Disconnect the new connection if there is already an active connection
        socketio.send('disconnect', {'msg': 'Connection already active.'})
        return False

    # Store the session ID of the active connection
    active_client_connection = request.sid


@socketio.on('init-simulation')
def handle_init_simulation():
    """
    init-simulation

    Sets up the simulation, with a model initialised in a background thread, ready to run
    """
    logger.info(json.dumps({
        'socket-event': 'init-simulation',
        'client id': request.sid,
        'active client id': active_client_connection,
    }, sort_keys=False, indent=4))

    global sim_manager
    if sim_manager and sim_manager.model_initialised is True:
        logger.error(json.dumps({
            'socket-event': 'init-simulation',
            'error': 'Model already initialised!',
        }, sort_keys=False, indent=4))

    # Setup a new simulation with the model initialised
    sim_manager = SimulationManager(socketio)
    sim_manager.init_simulation()

    logger.info(json.dumps({
        'socket-event': 'init-simulation',
        'simulation initialised': sim_manager.model_initialised,
        'model running': sim_manager.model_running,
    }, sort_keys=False, indent=4))


@socketio.on('continue-simulation')
def handle_start_simulation():
    """
    continue-simulation

    Resumes execution of the model running in the background
    """
    logger.info(json.dumps({
        'socket-event': 'continue-simulation',
        'client id': request.sid,
        'active client id': active_client_connection,
    }, sort_keys=False, indent=4))

    global sim_manager
    if not sim_manager or (sim_manager and not sim_manager.model_initialised):
        logger.error(json.dumps({
            'socket-event': 'continue-simulation',
            'error': 'Model not yet initialised! Run "Init" first',
        }, sort_keys=False, indent=4))

    # Resume the simulation run, executing the next step of an initialised model
    sim_manager.continue_simulation()

    logger.info(json.dumps({
        'socket-event': 'continue-simulation',
        'simulation initialised': sim_manager.model_initialised,
        'model running': sim_manager.model_running,
        'model step': sim_manager.current_step()
    }, sort_keys=False, indent=4))


@socketio.on('disconnect')
def handle_disconnection():
    """
    Disconnect

    The client can disconnect and then connect again, "resuming" the simulation as they left off
    We ensure only one client can be connected at a time
    """
    # global sim_manager
    # if sim_manager is not None:
    #     del sim_manager
    #     sim_manager = None

    global active_client_connection
    active_client_connection = None

    logger.info(json.dumps({
        'socket-event': 'disconnect',
        'client id': request.sid,
    }, sort_keys=False, indent=4))


if __name__ == '__main__':
    # Start the WebSocket server
    # socketio.run(app, host='localhost', port=9000)
    socketio.run(app, host='0.0.0.0')
