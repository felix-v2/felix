import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import Button from 'react-bootstrap/Button';
import { Card, Col, ProgressBar, Row } from 'react-bootstrap';
import ToggleButton from 'react-bootstrap/ToggleButton';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Potentials } from './components/potentials';
import { CellAssemblyOverlaps } from './components/cell-assembly-overlaps';
import { CellAssembly } from './components/cell-assembly';
import { ControlPanel } from './components/control-panel';
import { CellAssemblyPotentialsOverlaps } from './components/cell-assembly-potentials-overlaps';

const socket = io('ws://localhost:5000', { autoConnect: true });

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
 * @todo Refactor state into objects, use Zod schemas, validate in websocket handlers, and declare state locally
 * @todo Refactor socket-io interface https://socket.io/how-to/use-with-react
 * @todo Responsivity?
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

  /**
   * @todo refactor, this was hacked for demo purposes. should live in control
   */
  const [applySensoryInput, setApplySensoryInput] = useState<boolean>(true);
  const [applyMotorInput, setApplyMotorInput] = useState<boolean>(true);

  useEffect(() => {
    console.log('input change');
    socket.emit('update-config', {
      applySensoryInput,
      applyMotorInput,
    });
  }, [applySensoryInput, applyMotorInput]);

  // simulation functions
  useEffect(() => {
    if (running) {
      socket.emit('start-simulation', {
        applySensoryInput,
        applyMotorInput,
      });
    }

    if (connected && !running) {
      socket.emit('stop-simulation');
      // socket.disconnect();
      // socket.connect();
    }
  }, [socket, running]);

  useEffect(() => {
    socket.on('connect', () => {
      setConnected(true);
    });

    socket.on('disconnect', () => {
      setConnected(false);
      // setSensoryInput1(silence);
      // setArea1(silence);
      // setArea2(silence);
      // setArea3(silence);
      // setArea4(silence);
      // setArea5(silence);
      // setArea6(silence);
      // setMotorInput1(silence);
    });

    socket.on('new-activity', (data) => {
      console.log('New activity received from server', { area1: data.area1 });
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
            marginBottom: '30px',
            marginLeft: '100px',
            marginRight: '100px',
          }}
        >
          <Col xs={5}>
            <CellAssembly name={'CA #1'} activity={[]}></CellAssembly>
          </Col>
          <Col xs={5}>
            <CellAssembly name={'CA #2'} activity={[]}></CellAssembly>
          </Col>
        </Row>
        <Row
          style={{
            marginBottom: '30px',
            marginLeft: '100px',
            marginRight: '100px',
          }}
        >
          <Col xs={10}>
            <Potentials
              sensoryInput1={sensoryInput1}
              area1={area1}
              area2={area2}
              area3={area3}
              area4={area4}
              area5={area5}
              area6={area6}
              motorInput1={motorInput1}
            ></Potentials>
          </Col>
        </Row>
        <Row
          style={{
            marginBottom: '30px',
            marginLeft: '100px',
            marginRight: '100px',
          }}
        >
          <Col xs={5}>
            <CellAssemblyOverlaps activity={[]}></CellAssemblyOverlaps>
          </Col>
        </Row>
        <Row
          style={{
            marginBottom: '30px',
            marginLeft: '100px',
            marginRight: '100px',
          }}
        >
          <Col xs={7}>
            <CellAssemblyPotentialsOverlaps
              activity={[]}
            ></CellAssemblyPotentialsOverlaps>
          </Col>
        </Row>

        {/* MAIN SIMULATION MENU */}
        <Row style={{ marginBottom: '15px', marginLeft: '100px' }}>
          <Col xs={3}>
            <ToggleButton
              style={{ marginRight: '10px' }}
              variant={applySensoryInput ? 'primary' : 'outline-primary'}
              id="tbg-btn-1"
              value={1}
              checked={applySensoryInput}
              onClick={() => setApplySensoryInput(!applySensoryInput)}
            >
              Sensory input active
            </ToggleButton>
            <ToggleButton
              variant={applyMotorInput ? 'primary' : 'outline-primary'}
              id="tbg-btn-2"
              value={2}
              checked={applyMotorInput}
              onClick={() => setApplyMotorInput(!applyMotorInput)}
            >
              Motor input active
            </ToggleButton>
          </Col>
        </Row>
        <Row
          style={{
            marginTop: '50px',
            marginLeft: '100px',
            marginRight: '100px',
            marginBottom: '30px',
          }}
        >
          <Col xs={4}>
            <Card
              style={{
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
            >
              <Card.Header style={{ paddingTop: 15, paddingBottom: 15 }}>
                <Row>
                  <Col xs={6}>
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
                  <Col xs={6}>
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
                  onClick={() => setRunning(true)}
                  disabled={!connected || running}
                  variant="success"
                  size="sm"
                  style={{ marginRight: 10, width: '5rem' }}
                >
                  Start
                </Button>
                <Button
                  onClick={() => {
                    // @todo we want this to just stop receiving new activity, not necessarily disconnect
                    setRunning(false);
                    // setSensoryInput1(silence);
                    // setArea1(silence);
                    // setArea2(silence);
                    // setArea3(silence);
                    // setArea4(silence);
                    // setArea5(silence);
                    // setArea6(silence);
                    // setMotorInput1(silence);
                  }}
                  disabled={!connected || !running}
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
      </Col>
      ;
    </div>
  );
}
