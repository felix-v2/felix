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
            if self.model_running or self.model_initialised:
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
            # Check for updated config from the main thread
            if not self.config_queue.empty():
                config_change = self.config_queue.get()
                param = config_change['param']
                value = config_change['value']
                if param == 'noise':
                    self.model.config_set_noise(value)
                elif param == 'global-inhibition':
                    self.model.config_set_global_inhibition(value)
                elif param == 'pattern-number':
                    self.model.config_set_pattern_number(value)
                elif param == 'is-receiving-sensory-input':
                    self.model.config_set_is_receiving_sensory_input(value)
                elif param == 'is-receiving-motor-input':
                    self.model.config_set_is_receiving_motor_input(value)
                elif param == 'sensory-stimulation-amplitude':
                    self.model.config_set_sensory_stimulation_amplitude(value)
                elif param == 'motor-stimulation-amplitude':
                    self.model.config_set_motor_stimulation_amplitude(value)

            current_activity = self.model.step()
            self.socket.emit('new-activity', {
                'currentStep': current_activity['currentStep'],
                'totalActivity': current_activity['totalActivity'],
                'sensoryInput1': current_activity['sensInput'],
                'motorInput1': current_activity['motorInput'],
                'potentials': current_activity['potentials'],
                'globalInhibition': current_activity['globalInhibition'],
            })
            time.sleep(0.01)

    def update_config_parameter(self, param, new_value):
        with self.simulation_lock:
            self.config_queue.put({'param': param, 'value': new_value})

    def current_step(self):
        return self.model.stp
