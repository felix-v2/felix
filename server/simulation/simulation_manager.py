import threading
import time
from queue import Queue
from flask_socketio import SocketIO
from ..models.standardNet6Areas import StandardNet6Areas
import logging
import json

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger('simulation-manager')
logger.setLevel(logging.DEBUG)


# Interface between the socket layer and the model
# Handles threading and queueing to allow realtime bidirectional between the neural net and the gui
# Gives us a generic socket interface/server, into which we can plug and pull different neural networks as we wish
class SimulationManager:
    def __init__(self, socket):
        self.socket: SocketIO = socket

        self.config_queue = Queue()
        self.simulation_lock = threading.Lock()
        self.simulation_condition = threading.Condition(self.simulation_lock)
        self.simulation_thread = None

        self.model = StandardNet6Areas()
        self.model.main_init()

        self.model_initialised = False
        self.model_running = False

    def init_simulation(self):
        """
        Initialises the model to run in a background thread

        Init ->
        """
        with self.simulation_lock:
            if self.model_running:
                logger.error(json.dumps({
                    'op': 'init_simulation',
                    'error': 'Cannot start simulation: model already running!',
                }, sort_keys=False, indent=4))
                return

            logger.info(json.dumps({
                'op': 'init_simulation',
                'info': 'Initialising model in background',
            }, sort_keys=False, indent=4))

            self.model.init()
            self.model_initialised = True

            simulation_thread = threading.Thread(
                target=self.execute_model)
            simulation_thread.start()

    def continue_simulation(self):
        with self.simulation_lock:
            if not self.model_running:
                self.model_running = True
                self.simulation_condition.notify_all()

    def execute_model(self):
        with self.simulation_condition:
            while not self.model_running:
                self.simulation_condition.wait()

        while self.model_running:
            current_activity = self.model.step()
            self.socket.emit('new-activity', {
                'currentStep': current_activity['currentStep'],
                'sensoryInput1': current_activity['sensInput'],
                'motorInput1': current_activity['motorInput'],
                'area1': current_activity['area1'],
                'area2': current_activity['area2'],
                'area3': current_activity['area3'],
                'area4': current_activity['area4'],
                'area5': current_activity['area5'],
                'area6': current_activity['area6'],
            })
            time.sleep(0.01)

    def current_step(self):
        return self.model.stp
