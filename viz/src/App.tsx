import { useEffect, useState } from 'react';
import { Heatmap } from './Heatmap';
import { io } from 'socket.io-client';

const socket = io('ws://localhost:8080', { autoConnect: false });

export default function App() {
  const [message, setMessage] = useState('');
  const [messageFromServer, setMessageFromServer] = useState('');

  const connectWithMessage = () => {
    if (!socket.connected) {
      socket.connect();
    }
    socket.emit('msg-from-client', { message });
  };

  useEffect(() => {
    socket.on('connection', () => {
      console.log('Connected to server!');
    });

    socket.on('msg-from-server', (data) => {
      console.log('Message from server:', JSON.stringify(data));
      setMessageFromServer(data.message);
    });
  }, [socket]);

  return (
    <div className="App">
      <input
        placeholder="Message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      ></input>
      <button onClick={connectWithMessage}>Send message to server</button>
      <h1>Message from server: {messageFromServer}</h1>
      <div id="heatmap"></div>
      <Heatmap />
    </div>
  );
}
