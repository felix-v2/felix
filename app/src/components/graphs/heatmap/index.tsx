import Plot from 'react-plotly.js';

export const Heatmap = ({
  activity,
  title,
  height = 90,
  width = height,
}: {
  activity: number[][];
  title: string;
  width?: number;
  height?: number;
}) => {
  // scales the value domain (min neural activation - max neural activation) to a colour range
  const colourScale: Plotly.ColorScale = [
    [0, '#b0ceff'],
    [1, '#0a2f6b'],
  ];

  const data: Plotly.Data[] = [
    {
      type: 'heatmap',
      z: activity,
      colorscale: colourScale,
      showscale: false,
      hoverinfo: 'none',
      showlegend: false,
      mode: 'none',
      hovertext: 'none',
      hovertemplate: '',
    },
  ];

  return (
    <>
      <Plot
        config={{ displayModeBar: false, editable: false, staticPlot: true }}
        style={{
          marginLeft: 'auto',
          marginRight: 'auto',
        }}
        data={data}
        layout={{
          plot_bgcolor: '#e2e3e5',
          showlegend: false,
          margin: { t: 0, b: 0, l: 0, r: 0 },
          hidesources: true,
          height,
          width,
          xaxis: {
            showgrid: false,
            zeroline: false,
            visible: false,
          },
          yaxis: {
            automargin: true,
            showgrid: false,
            zeroline: false,
            visible: false,
          },
        }}
      />
    </>
  );
};
