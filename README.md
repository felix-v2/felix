# Running the Flask server

Dependencies:

- Python 3.9.6
- Pip 23.3.2
- Flask 3.0.0
- Flask SocketIO 5.3.6

Run server:
  
`python3 server/server.py`

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

## Rebuilding the neural net

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