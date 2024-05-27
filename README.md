# Running the simulation server

Dependencies:

- Python 3.9.6
- Pip 23.3.2
- Flask 3.0.0
- Flask SocketIO 5.3.6

# Run server from the repo root:
  
```bash
python3 -m server.simulation.simulation_server
```

# Running model unit tests

```bash
cd server
python3 -m unittest

# running a specific suite/file
python3 -m unittest models.__tests__.test_init_kernels
```

# Running the React app

Dependencies:

- Node 20.6.0
- NPM 9.8.1
- (react-scripts 5.0.1)

```
npm install
npm start
```

# Docker

## Initialising the whole Felix toolbox

Install Docker desktop.

Note: when docker builds the image, the node_modules directory is created within the container's app directory, and all the dependencies are installed there. Then on runtime the app directory from outside docker (the app on the host machine,with no installed node_modules) is mounted into the docker instance, essentially overwriting the node_modules that were just installed within the container.

Running npm i on the host machine, before running docker compose, mitigates this. But is there a more conventional way to do this?

https://stackoverflow.com/questions/30043872/docker-compose-node-modules-not-present-in-a-volume-after-npm-install-succeeds

```
npm i
docker-compose up
```

## Modifying the GUI

Due to a combination of hot reloads (by the Create React App library) and the mounting of the app as a volume onto its container, you can make changes to the React application whilst it's running, and once you save a file, you will see your changes reflected almost instantly.

## Modifying the neural net

To start with, we will not enable hot reloading for the Python backend. Hot reloads - auto-reloading the server - will destroy any in-progress simulation.

Instead you can make change to the Python backend and neural net anytime you like, even during a simulation run, but your changes will not take effect until you manually rebuild the backend image and serve it to its container.

When you want to do this, you should run the following commands:

```
docker-compose down
docker build --tag felix-server ./server
docker-compose up
```

## Spinning up the apps (server and gui) individually

### Server

```
docker build --tag felix-server ./server
docker run --name felix-server -d -p 5000:5000 felix-server
```

### GUI

```
docker build --tag felix-gui ./app
docker run --name felix-gui -d -p 3000:3000 felix-gui
```