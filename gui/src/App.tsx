import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import Plot from 'react-plotly.js';
import Button from 'react-bootstrap/Button';
import {
  Accordion,
  Card,
  Col,
  Form,
  Offcanvas,
  ProgressBar,
  Row,
} from 'react-bootstrap';
import RangeSlider from 'react-bootstrap-range-slider';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';

const socket = io('ws://localhost:8080', { autoConnect: true });

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
    socket.disconnect();
    socket.connect();
    socket.emit('start-simulation');
  };

  useEffect(() => {
    if (running) {
      startSimulation();
    } else {
      socket.disconnect();
    }
  }, [running]);

  useEffect(() => {
    socket.on('connect', () => {
      setConnected(true);
    });

    socket.on('disconnect', () => {
      setConnected(false);
    });

    socket.on('new-activity', (data) => {
      if (!running) return;
      setSensoryInput1(data.sensoryInput1);
      setArea1(data.area1);
      setArea2(data.area2);
      setArea3(data.area3);
      setArea4(data.area4);
      setArea5(data.area5);
      setArea6(data.area6);
      setMotorInput1(data.motorInput1);
    });
  }, [socket, connected]);

  return (
    <div className="App">
      <Col style={{ marginTop: '30px' }}>
        <Row
          style={{
            marginTop: '30px',
            marginLeft: '100px',
            marginRight: '100px',
            marginBottom: '30px',
          }}
        >
          <Col sm={4}>
            <Card
              style={{
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
            >
              <Card.Header style={{ paddingTop: 15, paddingBottom: 15 }}>
                <Row>
                  <Col sm={6}>
                    <Button
                      onClick={() => setShowControlPanel(true)}
                      variant="outline-dark"
                      size="sm"
                    >
                      Control Panel
                    </Button>
                  </Col>
                  <ControlPanel
                    visible={showControlPanel}
                    onHide={() => setShowControlPanel(false)}
                  ></ControlPanel>
                  <Col sm={6}>
                    <ProgressBar
                      style={{ height: '2rem' }}
                      animated
                      variant={connected ? 'success' : 'danger'}
                      now={100}
                      label={
                        connected
                          ? 'Neural net connection live'
                          : 'Not connected to neural net'
                      }
                    />
                  </Col>
                </Row>
              </Card.Header>
              <Card.Body>
                <Card.Title>Simulation</Card.Title>
                <Button
                  onClick={() => {
                    setRunning(true);
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
                  }}
                  disabled={!running}
                  variant="danger"
                  size="sm"
                  style={{ marginRight: 5, width: '5rem' }}
                >
                  Stop
                </Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>
        <Row
          style={{
            marginBottom: '30px',
            marginLeft: '20px',
            marginRight: '20px',
          }}
        >
          <Col sm={6}>
            <Accordion
              defaultActiveKey="0"
              style={{
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
            >
              <Accordion.Item eventKey="0">
                <Accordion.Header>CA #1</Accordion.Header>
                <Accordion.Body style={{ paddingTop: 30, paddingBottom: 30 }}>
                  <Row>
                    <Col>{Heatmap({ title: 'Area 1', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 2', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 3', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 4', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 5', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 6', activity: silence })}</Col>
                  </Row>
                </Accordion.Body>
              </Accordion.Item>
            </Accordion>
          </Col>
          <Col sm={6}>
            <Accordion
              defaultActiveKey="0"
              style={{
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
            >
              <Accordion.Item eventKey="0">
                <Accordion.Header>CA #2</Accordion.Header>
                <Accordion.Body style={{ paddingTop: 30, paddingBottom: 30 }}>
                  <Row>
                    <Col>{Heatmap({ title: 'Area 1', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 2', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 3', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 4', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 5', activity: silence })}</Col>
                    <Col>{Heatmap({ title: 'Area 6', activity: silence })}</Col>
                  </Row>
                </Accordion.Body>
              </Accordion.Item>
            </Accordion>
          </Col>
        </Row>
        <Row
          style={{
            marginBottom: '30px',
            marginLeft: '100px',
            marginRight: '100px',
          }}
        >
          <Col>
            <Accordion
              defaultActiveKey="0"
              style={{
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
            >
              <Accordion.Item eventKey="0">
                <Accordion.Header>CA #1</Accordion.Header>
                <Accordion.Body style={{ paddingTop: 30, paddingBottom: 30 }}>
                  <Row>
                    <Col>
                      {Heatmap({
                        title: 'Sensory Input 1',
                        activity: sensoryInput1,
                        size: 150,
                      })}
                    </Col>
                    <Col>
                      {Heatmap({ title: 'Area 1', activity: area1, size: 150 })}
                    </Col>
                    <Col>
                      {Heatmap({ title: 'Area 2', activity: area2, size: 150 })}
                    </Col>
                    <Col>
                      {Heatmap({ title: 'Area 3', activity: area3, size: 150 })}
                    </Col>
                    <Col>
                      {Heatmap({ title: 'Area 4', activity: area4, size: 150 })}
                    </Col>
                    <Col>
                      {Heatmap({ title: 'Area 5', activity: area5, size: 150 })}
                    </Col>
                    <Col>
                      {Heatmap({ title: 'Area 6', activity: area6, size: 150 })}
                    </Col>
                    <Col>
                      {Heatmap({
                        title: 'Motor Input 1',
                        activity: motorInput1,
                        size: 150,
                      })}
                    </Col>
                  </Row>
                </Accordion.Body>
              </Accordion.Item>
            </Accordion>
          </Col>
        </Row>
      </Col>
      ;
    </div>
  );
}

/**
 * @todo move to separate file
 */
const Heatmap = ({
  activity,
  title,
  size = 100,
}: {
  activity: number[][];
  title: string;
  size?: number;
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
          height: size,
          width: size,
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
          width: size,
          marginLeft: 'auto',
          marginRight: 'auto',
          marginTop: '10px',
        }}
        variant="outline-primary"
        size="sm"
      >
        {title}
      </Button>
    </>
  );
};

/**
 * @todo move to separate file
 */
const ControlPanel = ({
  visible,
  onHide,
}: {
  visible: boolean;
  onHide: () => void;
}) => {
  const [io, setIo] = useState<number>(0);
  const [noise, setNoise] = useState<number>(0);
  const [steps, setSteps] = useState<number>(0);
  const [displaySteps, setDisplaySteps] = useState<number>(0);
  const [sensoryInputRow, setSensoryInputRow] = useState<number>(0);
  const [sensoryInputCol, setSensoryInputCol] = useState<number>(0);
  const [motorInputRow, setMotorInputRow] = useState<number>(0);
  const [motorInputCol, setMotorInputCol] = useState<number>(0);
  const [gain, setGain] = useState<number>(0);
  const [theta, setTheta] = useState<number>(0);
  const [sensoryStimAmp, setSensoryStimAmp] = useState<number>(0);
  const [motorStimAmp, setMotorStimAmp] = useState<number>(0);
  const [pattern, setPattern] = useState<number>(0);
  const [learn, setLearn] = useState<number>(0);
  const [diluteProb, setDiluteProb] = useState<number>(0);
  const [diluteArea, setDiluteArea] = useState<number>(0);
  const [jFfb, setJffb] = useState<number>(0);
  const [jRec, setJRec] = useState<number>(0);
  const [jInh, setJInh] = useState<number>(0);
  const [jSlow, setJSlow] = useState<number>(0);

  return (
    <Offcanvas
      show={visible}
      onHide={onHide}
      placement="bottom"
      scroll={true}
      style={{ height: '60%' }}
    >
      <Offcanvas.Header closeButton>
        <Offcanvas.Title>Control Panel</Offcanvas.Title>
      </Offcanvas.Header>
      <Offcanvas.Body>
        <Row>
          <Col lg={3}>
            <Slider
              title="IO"
              min={-1000}
              max={1000}
              value={io}
              setValue={setIo}
            ></Slider>
            <Slider
              title="Noise"
              min={0}
              max={1000}
              value={noise}
              setValue={setNoise}
            ></Slider>
            <Slider
              title="Steps"
              min={1}
              max={100}
              value={steps}
              setValue={setSteps}
            ></Slider>
            <Slider
              title="Display steps"
              min={1}
              max={100}
              value={displaySteps}
              setValue={setDisplaySteps}
            ></Slider>
            <Slider
              title="Jffb"
              min={0}
              max={5000}
              value={jFfb}
              setValue={setJffb}
            ></Slider>
          </Col>
          <Col lg={3}>
            <Slider
              title="Sensory input row"
              min={1}
              max={2}
              value={sensoryInputRow}
              setValue={setSensoryInputRow}
            ></Slider>
            <Slider
              title="Sensory input col"
              min={1}
              max={3}
              value={sensoryInputCol}
              setValue={setSensoryInputCol}
            ></Slider>
            <Slider
              title="Motor input row"
              min={1}
              max={2}
              value={motorInputRow}
              setValue={setMotorInputRow}
            ></Slider>
            <Slider
              title="Motor input col"
              min={1}
              max={6}
              value={motorInputCol}
              setValue={setMotorInputCol}
            ></Slider>
            <Slider
              title="Jrec"
              min={0}
              max={5000}
              value={jRec}
              setValue={setJRec}
            ></Slider>
          </Col>
          <Col lg={3}>
            <Slider
              title="Gain"
              min={0}
              max={5000}
              value={gain}
              setValue={setGain}
            ></Slider>
            <Slider
              title="Theta"
              min={0}
              max={5000}
              value={theta}
              setValue={setTheta}
            ></Slider>
            <Slider
              title="Sensory stim. amp"
              min={0}
              max={1000}
              value={sensoryStimAmp}
              setValue={setSensoryStimAmp}
            ></Slider>
            <Slider
              title="Motor stim. amp"
              min={0}
              max={1000}
              value={motorStimAmp}
              setValue={setMotorStimAmp}
            ></Slider>
            <Slider
              title="Jinh"
              min={0}
              max={5000}
              value={jInh}
              setValue={setJInh}
            ></Slider>
          </Col>
          <Col lg={3}>
            <Slider
              title="Pattern #"
              min={0}
              max={13}
              value={pattern}
              setValue={setPattern}
            ></Slider>
            <Slider
              title="Learn"
              min={0}
              max={1000}
              value={learn}
              setValue={setLearn}
            ></Slider>
            <Slider
              title="Dilute prob"
              min={0}
              max={100}
              value={diluteProb}
              setValue={setDiluteProb}
            ></Slider>
            <Slider
              title="Dilute area"
              min={0}
              max={6}
              value={diluteArea}
              setValue={setDiluteArea}
            ></Slider>
            <Slider
              title="J-slow"
              min={0}
              max={5000}
              value={jSlow}
              setValue={setJSlow}
            ></Slider>
          </Col>
        </Row>
      </Offcanvas.Body>
    </Offcanvas>
  );
};

/**
 * @todo move to separate file
 */
const Slider = ({
  title,
  min,
  max,
  value,
  setValue,
}: {
  title: string;
  min: number;
  max: number;
  value: number;
  setValue: (v: number) => void;
}) => {
  return (
    <Form style={{ marginTop: '10px', marginRight: '10px' }}>
      <Form.Group as={Row}>
        <Form.Label>{title}</Form.Label>
        <Col xs="8">
          <RangeSlider
            value={value}
            min={min}
            max={max}
            onChange={(e) => setValue(Number(e.target.value))}
          />
        </Col>
        <Col xs="4">
          <Form.Control
            size="sm"
            value={`${value} / ${max}`}
            disabled={false}
          />
        </Col>
      </Form.Group>
    </Form>
  );
};
