import threading
import time
from queue import Queue
from abc import ABC, abstractmethod
from flask_socketio import SocketIO


# All we need to do is ensure the actual neural net - StandardArea6Net - adheres to this "interface"
# Then in simulation-server.py we can instantiate it and pass it to the SimulationManager
# SimulationManager(standardNet6Areas, socket)
class Model(ABC):

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def update_config(self, new_config):
        pass


# Interface between the socket layer and the model
# Handles threading and queueing to allow realtime bidirectional between the neural net and the gui
# Gives us a generic socket interface/server, into which we can plug and pull different neural networks as we wish
class SimulationManager:
    def __init__(self, model, socket):
        self.model: Model = model
        self.socket: SocketIO = socket

        self.config_queue = Queue()
        self.simulation_lock = threading.Lock()
        self.simulation_running = False
        self.simulation_thread = None

    # todo: reinstantiate the model?
    def reset_simulation(self):
        pass

    # todo: I think it's ok to stop and start the tread like this and maintain the model state over time
    # e.g. restarting the thread doesn't reset the model state
    def start_simulation(self, config):

        with self.simulation_lock:
            self.config_queue.put(config)

            if not self.simulation_running:
                self.simulation_running = True
                simulation_thread = threading.Thread(
                    target=self.execute_model)
                simulation_thread.start()
                print('Simulation started!')

            print('Simulation-start request received but simulation already running!')

    def stop_simulation(self):
        with self.simulation_lock:
            if self.simulation_running:
                self.simulation_running = False
                print('Simulation stopped!')

            print('Simulation-stop request received but simulation is not running!')

    def resume_simulation(self, config):
        self.start_simulation(config)

    def update_config(self, new_config):
        with self.simulation_lock:
            if self.simulation_running:
                self.config_queue.put(new_config)
            print('Update-config request received but simulation is not running!')

    def execute_model(self):
        while self.simulation_running:
            # Check for updated config from the main thread
            if not self.config_queue.empty():
                new_config = self.config_queue.get()
                self.model.update_config(new_config)

            # Perform simulation computation using simulation_config
            result_data = self.model.step()

            # Send the result_data to the client
            self.socket.emit('new-activity', result_data)

            # Sleep to simulate a delay between steps
            time.sleep(1)

        print('Execute-model request received but simulation is not running!')
