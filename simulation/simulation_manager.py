import threading
import time
from queue import Queue


class SimulationManager:
    def __init__(self, model, socket):
        self.model = model
        self.socket = socket

        self.config_queue = Queue()
        self.simulation_running = False
        self.simulation_lock = threading.Lock()

    def start_simulation(self):
        with self.simulation_lock:
            if not self.simulation_running:
                self.simulation_running = True
                simulation_thread = threading.Thread(
                    target=self.execute_model)
                simulation_thread.start()

    def stop_simulation(self):
        with self.simulation_lock:
            self.simulation_running = False

    def update_config(self, new_config):
        self.config_queue.put(new_config)

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
