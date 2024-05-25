import { useEffect, useState } from 'react';
import { socket, InboundEvent } from './socket';
import { Col, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Potentials } from './sections/potentials';
import { CellAssemblyOverlaps } from './sections/cell-assembly-overlaps';
import { CellAssembly } from './sections/cell-assembly';
import { CellAssemblyPotentialsOverlaps } from './sections/cell-assembly-potentials-overlaps';
import { ControlPanel } from './sections/control-panel';
import { Totals } from './sections/totals';
import { randActivity } from './util';
import TransientToast from './components/toast';

/**
 * @todo Refactor state into objects, use Zod schemas, validate in websocket handlers, and declare state locally
 * @todo Responsivity?
 */
export default function App() {
  // server connection
  const [connected, setConnected] = useState(socket.connected);

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

  useEffect(() => {
    const onConnect = () => {
      setConnected(true);
    };

    const onDisconnect = () => {
      setArea1(silence);
      setArea2(silence);
      setArea3(silence);
      setArea4(silence);
      setArea5(silence);
      setArea6(silence);

      setSensoryInput1(sensoryInput1);
      setMotorInput1(motorInput1);

      setConnected(false);
    };

    const onNewActivity = (data: any) => {
      setSensoryInput1(data.sensoryInput1);
      setMotorInput1(data.motorInput1);

      setArea1(data.area1);
      setArea2(data.area2);
      setArea3(data.area3);
      setArea4(data.area4);
      setArea5(data.area5);
      setArea6(data.area6);
    };

    socket.on(InboundEvent.Connect, onConnect);
    socket.on(InboundEvent.Disconnect, onDisconnect);
    socket.on(InboundEvent.NewActivity, onNewActivity);

    return () => {
      socket.off(InboundEvent.Connect, onConnect);
      socket.off(InboundEvent.Disconnect, onDisconnect);
      socket.off(InboundEvent.NewActivity, onNewActivity);
    };
  }, []);

  return (
    <div className="App">
      {/* <TransientToast error={true} /> */}
      <ControlPanel
        visible={true}
        connectedToServer={connected}
        onHide={() => console.log('Hide')}
      />
      <Col xs={10} style={{ marginTop: '40px' }}>
        <Row
          style={{
            marginBottom: '50px',
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
            marginBottom: '50px',
            marginLeft: '5px',
            marginRight: '100px',
          }}
        >
          <Col xs={12}>
            <Potentials
              sensoryInput1={sensoryInput1}
              motorInput1={motorInput1}
              area1={area1}
              area2={area2}
              area3={area3}
              area4={area4}
              area5={area5}
              area6={area6}
            ></Potentials>
          </Col>
        </Row>
        <Row
          style={{
            marginBottom: '50px',
            marginLeft: '5px',
            marginRight: '100px',
          }}
        >
          <Totals />
        </Row>
        <Row
          style={{
            marginBottom: '50px',
            marginLeft: '5px',
            marginRight: '100px',
          }}
        >
          <Col xs={6}>
            <CellAssemblyOverlaps activity={[]}></CellAssemblyOverlaps>
          </Col>
        </Row>
        <Row
          style={{
            marginBottom: '50px',
            marginLeft: '5px',
            marginRight: '100px',
          }}
        >
          <Col xs={8}>
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
