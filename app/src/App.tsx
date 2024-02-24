import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { Col, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Potentials } from './components/potentials';
import { CellAssemblyOverlaps } from './components/cell-assembly-overlaps';
import { CellAssembly } from './components/cell-assembly';
import { CellAssemblyPotentialsOverlaps } from './components/cell-assembly-potentials-overlaps';
import { ControlPanel } from './components/control-panel';

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
      <ControlPanel visible={true} onHide={() => console.log('Hide')} />
      <Col xs={10} style={{ marginTop: '40px' }}>
        <Row
          style={{
            marginBottom: '30px',
            marginLeft: '5px',
            marginRight: '100px',
          }}
        >
          <Col xs={6}>
            <CellAssembly name={'CA #1'} activity={[]}></CellAssembly>
          </Col>
          <Col xs={6}>
            <CellAssembly name={'CA #2'} activity={[]}></CellAssembly>
          </Col>
        </Row>
        <Row
          style={{
            marginBottom: '30px',
            marginLeft: '5px',
            marginRight: '100px',
          }}
        >
          <Col xs={12}>
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
            marginLeft: '5px',
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
            marginLeft: '5px',
            marginRight: '100px',
          }}
        >
          <Col xs={7}>
            <CellAssemblyPotentialsOverlaps
              activity={[]}
            ></CellAssemblyPotentialsOverlaps>
          </Col>
        </Row>
      </Col>
      ;
    </div>
  );
}
