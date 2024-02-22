import Plot from 'react-plotly.js';

// Function to compute values of normal distribution
const normalDistribution = (x: number, mean: number, stdDev: number) => {
  return (
    (1 / (stdDev * Math.sqrt(2 * Math.PI))) *
    Math.exp(-Math.pow(x - mean, 2) / (2 * Math.pow(stdDev, 2)))
  );
};

export const LineGraph = () => {
  const xData = Array.from({ length: 151 }, (_, index) => index);

  // Generate yData representing a normal distribution with mean 50 and standard deviation 10
  const mean = 50;
  const stdDev = 10;
  const yData = xData.map((x) => normalDistribution(x, mean, stdDev));

  return (
    <Plot
      config={{ displayModeBar: false, editable: false, staticPlot: true }}
      data={[
        {
          x: xData,
          y: yData,
          type: 'scatter',
          mode: 'lines',
          marker: { color: 'black' },
          line: { width: 1 },
          hoverinfo: 'none',
          showlegend: false,
          hovertext: 'none',
          hovertemplate: '',
        },
      ]}
      layout={{
        height: 200,
        width: 300,
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
