import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import Plot from 'react-plotly.js';

const socket = io('ws://localhost:8080', { autoConnect: false });

// generates a 2d matrix of X x Y neurons, each with a random activity value between 0 and 1
export const randActivity = (
  opts: {
    neuronsX?: number;
    neuronsY?: number;
    silent?: boolean;
  } = { neuronsX: 25, neuronsY: 25 },
) => {
  return Array.from(Array(opts.neuronsX)).map(() =>
    Array.from(Array(opts.neuronsY)).map(() =>
      opts.silent ? 0 : Math.random(),
    ),
  );
};

export default function App() {
  const [activity, setActivity] = useState(randActivity({ silent: true }));

  const connect = () => {
    if (!socket.connected) {
      socket.connect();
    }
  };

  const disconnect = () => {
    socket.disconnect();
  };

  useEffect(() => {
    socket.on('connection', () => {
      console.log('Connected to server!');
    });

    socket.on('new-activity', (data) => {
      console.log('Activity from server');
      setActivity(data);
    });
  }, [socket]);

  // scales the value domain (min neural activation - max neural activation) to a colour range
  const colourScale: Plotly.ColorScale = [
    [0, '#3D9970'],
    [1, '#001f3f'],
  ];

  const data: Plotly.Data[] = [
    {
      type: 'heatmap',
      z: activity,
      colorscale: colourScale,
      showscale: false,
      showlegend: false,
      hoverinfo: 'none',
      mode: 'none',
      hovertext: 'none',
    },
  ];

  return (
    <div className="App">
      <button onClick={connect}>Start</button>
      <button onClick={disconnect}>Stop</button>
      <div>
        <Plot
          data={data}
          layout={{ width: 500, height: 500, title: 'Area 1' }}
        />
      </div>
    </div>
  );
}
