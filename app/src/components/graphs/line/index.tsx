import Plot from 'react-plotly.js';

// Function to compute values of normal distribution
const normalDistribution = (x: number, mean: number, stdDev: number) => {
  return (
    (1 / (stdDev * Math.sqrt(2 * Math.PI))) *
    Math.exp(-Math.pow(x - mean, 2) / (2 * Math.pow(stdDev, 2)))
  );
};

export const TimeSeriesGraph = ({ title }: { title: string }) => {
  const xData = Array.from({ length: 151 }, (_, index) => index);
  const mean = 50;
  const stdDev = 10;
  const yData = xData.map((x) => normalDistribution(x, mean, stdDev));

  return (
    <Plot
      style={{ width: '300px', height: '200px' }}
      config={{ displayModeBar: false, editable: false, staticPlot: true }}
      data={[
        {
          x: xData,
          y: yData,
          type: 'scatter',
          mode: 'lines',
          marker: { color: 'blue' },
          line: { width: 1 }, // Adjust line width,
          hoverinfo: 'none',
          showlegend: false,
          hovertext: 'none',
          hovertemplate: '',
        },
      ]}
      layout={{
        xaxis: {
          showgrid: false,
          zeroline: false,
          visible: false,
        },
        yaxis: {
          showgrid: false,
          zeroline: false,
          visible: false,
        },
      }}
    />
  );
};
