import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import Plot from 'react-plotly.js';
import Button from 'react-bootstrap/Button';
import {
  Card,
  Col,
  Offcanvas,
  Pagination,
  ProgressBar,
  Row,
} from 'react-bootstrap';

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

/**
 * @todo Refactor into composable components
 * @todo Add Zod parsing to WebSocket handlers on both client and server
 * @todo Make responsive
 * @todo Remove bloody controls from Plotly heatmap (appears on hover)
 * @todo Add sensory and motor inputs
 * @todo Have the heatmaps respond correctly to server connection/disconnection
 */
export default function App() {
  // server connection
  const [connected, setConnected] = useState(socket.connected);
  const [running, setRunning] = useState(false);
  const [stepDuration, setStepDuration] = useState(1000);

  // activity
  const silence = randActivity({ silent: true });

  const [sensoryInput1, setSensoryInput1] = useState<number[][]>(silence);
  const [area1, setArea1] = useState<number[][]>(silence);
  const [area2, setArea2] = useState<number[][]>(silence);
  const [area3, setArea3] = useState<number[][]>(silence);
  const [area4, setArea4] = useState<number[][]>(silence);
  const [area5, setArea5] = useState<number[][]>(silence);
  const [area6, setArea6] = useState<number[][]>(silence);
  const [motorInput1, setMotorInput1] = useState<number[][]>(silence);

  // control panel
  const [showControlPanel, setShowControlPanel] = useState(false);

  // simulation functions
  const startSimulation = () => {
    stopSimulation();
    socket.connect();
    socket.emit('start-simulation', { stepDuration });
  };

  const stopSimulation = () => {
    socket.disconnect();
  };

  useEffect(() => {
    socket.on('connect', () => {
      console.log('Connected to server!');
      setConnected(true);
    });

    socket.on('disconnect', () => {
      stopSimulation();
    });

    socket.on('new-activity', (data) => {
      console.log('Activity from server with step duration', {
        serverStepDuration: data.stepDuration,
        clientStepDuration: stepDuration,
      });

      if (data.stepDuration === stepDuration) {
        setSensoryInput1(data.sensoryInput1);
        setArea1(data.area1);
        setArea2(data.area2);
        setArea3(data.area3);
        setArea4(data.area4);
        setArea5(data.area5);
        setArea6(data.area6);
        setMotorInput1(data.motorInput1);
      }
    });
  }, [socket, stepDuration, connected]);

  useEffect(() => {
    startSimulation();
  }, [stepDuration]);

  return (
    <div className="App">
      <Col
        style={{ marginLeft: '100px', marginRight: '100px', marginTop: '50px' }}
      >
        <Row style={{ marginBottom: 20 }}>
          <Col sm={10}>
            <Button
              variant="outline-dark"
              size="sm"
              onClick={() => setShowControlPanel(true)}
            >
              Control Panel
            </Button>
            <ControlPanel
              visible={showControlPanel}
              onHide={() => setShowControlPanel(false)}
            ></ControlPanel>
          </Col>
          <Col sm={2} offset={10}>
            <ProgressBar
              style={{ height: '2rem' }}
              animated
              variant={connected ? 'success' : 'danger'}
              now={100}
              label={
                connected ? 'Connected to server' : 'Not connected to server'
              }
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <Card
              style={{
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
            >
              <Card.Header style={{ paddingTop: 30, paddingBottom: 30 }}>
                <Row>
                  <Col>{Heatmap({ title: 'Area 1', activity: area1 })}</Col>
                  <Col>{Heatmap({ title: 'Area 2', activity: area2 })}</Col>
                  <Col>{Heatmap({ title: 'Area 3', activity: area3 })}</Col>
                  <Col>{Heatmap({ title: 'Area 4', activity: area4 })}</Col>
                  <Col>{Heatmap({ title: 'Area 5', activity: area5 })}</Col>
                  <Col>{Heatmap({ title: 'Area 6', activity: area6 })}</Col>
                </Row>
              </Card.Header>
              <Card.Body>
                <Card.Title>Current Network Activity</Card.Title>
                <Card.Text>
                  You can start a simulation at your chosen step duration, and
                  stop it anytime you like.
                </Card.Text>
                <Row>
                  <Col sm={2}>
                    <Pagination size="sm">
                      <Pagination.Item
                        active={stepDuration === 100}
                        onClick={() => {
                          setRunning(true);
                          setStepDuration(100);
                        }}
                      >
                        {100}
                      </Pagination.Item>
                      <Pagination.Item
                        active={stepDuration === 200}
                        onClick={() => {
                          setRunning(true);
                          setStepDuration(200);
                        }}
                      >
                        {200}
                      </Pagination.Item>
                      <Pagination.Ellipsis />
                      <Pagination.Item
                        active={stepDuration === 1000}
                        onClick={() => {
                          setRunning(true);
                          setStepDuration(1000);
                        }}
                      >
                        {1000}
                      </Pagination.Item>
                      <Pagination.Item
                        active={stepDuration === 2000}
                        onClick={() => {
                          setRunning(true);
                          setStepDuration(2000);
                        }}
                      >
                        {2000}
                      </Pagination.Item>
                    </Pagination>
                  </Col>
                  <Col sm={2}>
                    <Button
                      onClick={() => {
                        setRunning(true);
                        startSimulation();
                      }}
                      disabled={running}
                      variant="success"
                      size="sm"
                      style={{ marginRight: 10, width: '5rem' }}
                    >
                      Start
                    </Button>
                    <Button
                      onClick={() => {
                        setRunning(false);
                        stopSimulation();
                      }}
                      disabled={!running}
                      variant="danger"
                      size="sm"
                      style={{ marginRight: 5, width: '5rem' }}
                    >
                      Stop
                    </Button>
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Col>
      ;
    </div>
  );
}

const Heatmap = ({
  activity,
  title,
}: {
  activity: number[][];
  title: string;
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
      showlegend: false,
      hoverinfo: 'none',
      mode: 'none',
      hovertext: 'none',
    },
  ];

  return (
    <>
      <Plot
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
          height: 200,
          width: 200,
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
      <Button
        style={{
          width: 200,
          marginLeft: 'auto',
          marginRight: 'auto',
          marginTop: '10px',
        }}
        variant="outline-primary"
      >
        {title}
      </Button>
    </>
  );
};

const ControlPanel = ({
  visible,
  onHide,
}: {
  visible: boolean;
  onHide: () => void;
}) => {
  return (
    <Offcanvas show={visible} onHide={onHide}>
      <Offcanvas.Header closeButton>
        <Offcanvas.Title>Felix Control Panel</Offcanvas.Title>
      </Offcanvas.Header>
      <Offcanvas.Body>
        All the toggles and sliders for configuring the simulation parameters.
      </Offcanvas.Body>
    </Offcanvas>
  );
};
