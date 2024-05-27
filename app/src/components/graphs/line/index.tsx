import Plot from 'react-plotly.js';

const prepareDataForPlot = (data: number[]) => {
  const yData = data;
  const xData = data.map((_, i) => i);

  const mean = data.reduce((acc, val) => acc + val, 0) / data.length;

  const variance =
    data.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / data.length;
  const standardDeviation = Math.sqrt(variance);

  return { yData, xData, mean, standardDeviation };
};

export const TimeSeriesGraph = ({
  title,
  data,
}: {
  title: string;
  data: number[];
}) => {
  console.log({ data });
  const { xData, yData } = prepareDataForPlot(data);

  return (
    <Plot
      style={{ width: '300px', height: '200px', border: '1px' }}
      config={{ displayModeBar: false, editable: false, staticPlot: true }}
      data={[
        {
          x: xData,
          y: yData,
          type: 'scatter',
          mode: 'lines',
          marker: { color: 'black' },
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
          visible: true,
          tickvals: [],
        },
        yaxis: {
          showgrid: false,
          zeroline: true,
          visible: true,
          tickvals: [0, 3000],
        },
      }}
    />
  );
};
