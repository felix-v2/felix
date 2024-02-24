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
          mode: 'lines+markers',
          marker: { color: 'black' },
          line: { width: 0.2 },
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

export const TimeSeriesGraph = ({ title }: { title: string }) => {
  // // Sample time-series data
  // const timeSeriesData = [
  //   { date: '2022-01-01', value: 10 },
  //   { date: '2022-01-02', value: 15 },
  //   { date: '2022-01-03', value: 13 },
  //   { date: '2022-01-04', value: 17 },
  //   { date: '2022-01-05', value: 20 },
  // ];

  // // Extract x-axis (dates) and y-axis (values) data from timeSeriesData
  // const xData = timeSeriesData.map((data) => data.date);
  // const yData = timeSeriesData.map((data) => data.value);

  const xData = Array.from({ length: 151 }, (_, index) => index);

  // Generate yData representing a normal distribution with mean 50 and standard deviation 10
  const mean = 50;
  const stdDev = 10;
  const yData = xData.map((x) => normalDistribution(x, mean, stdDev));

  return (
    <Plot
      style={{ width: '300px', height: '200px', backgroundColor: 'black' }} // Adjust width and height
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
        title,
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
