import { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

// generates a 2d matrix of X x Y neurons, each with a random activity value between 0 and 1
const randActivity = (
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

const generateMatrixLabels = (neurons: number = 25) => {
  return Array.from(Array(neurons).keys()).map((_, i) => `N${i + 1}`);
};

// The main component for visualising simulated neural activity in a network
export const Heatmap = () => {
  const [activity, setActivity] = useState(randActivity({ silent: true }));

  // generate random activity matrix periodically and update the state
  useEffect(() => {
    setInterval(() => {
      setActivity(randActivity());
    }, 600);
  }, []);

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
    <div>
      <Plot data={data} layout={{ width: 500, height: 500, title: 'Area 1' }} />
    </div>
  );
};
