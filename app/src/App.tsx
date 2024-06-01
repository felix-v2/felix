import { useEffect, useState } from 'react';
import { socket, InboundEvent, OutboundEvent } from './socket';
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
  const [connected, setConnected] = useState(socket.connected);

  const [errorNotification, setErrorNotification] = useState<{
    show: boolean;
    msg: string;
  }>({ show: false, msg: '' });

  const [infoNotification, setInfoNotification] = useState<{
    show: boolean;
    msg: string;
  }>({ show: false, msg: '' });

  const silence = randActivity({ silent: true });
  const full = randActivity({ full: true });

  const [currentStep, setCurrentStep] = useState<number>(0);

  // control panel config
  const [patternNumber, setPatternNumber] = useState<number>(0);
  const [networkTrainingActivated, setNetworkTrainingActivated] =
    useState<boolean>(false);

  // time-series data (1 area, 1d)
  const [totalActivity, setTotalActivity] = useState<number[]>([]);
  const [globalInhibition, setGlobalInhibition] = useState<number[]>([]);

  // neural activity (1 area, 2d)
  const [sensoryInput1, setSensoryInput1] = useState<number[][]>(full);
  const [motorInput1, setMotorInput1] = useState<number[][]>(full);

  // neural activity (1 area, 2d)
  const [area1, setArea1] = useState<number[][]>(silence);
  const [area2, setArea2] = useState<number[][]>(silence);
  const [area3, setArea3] = useState<number[][]>(silence);
  const [area4, setArea4] = useState<number[][]>(silence);
  const [area6, setArea6] = useState<number[][]>(silence);
  const [area5, setArea5] = useState<number[][]>(silence);

  useEffect(() => {
    const onConnect = () => {
      setConnected(true);
    };

    const onDisconnect = () => {
      setConnected(false);
    };

    const onNewActivity = (data: any) => {
      setCurrentStep(data.currentStep);
      console.log(data.config);

      setPatternNumber(data.config.patternNumber);
      setNetworkTrainingActivated(data.config.networkTrainingActivated);

      setTotalActivity((prevTotalActivity) => {
        const updatedArray = [...prevTotalActivity, data.totalActivity];
        return updatedArray.length > 100 ? updatedArray.slice(1) : updatedArray;
      });

      setGlobalInhibition((prevGlobalInhibition) => {
        const updatedArray = [
          ...prevGlobalInhibition,
          data.globalInhibition.area1,
        ];
        return updatedArray.length > 100 ? updatedArray.slice(1) : updatedArray;
      });

      setSensoryInput1(data.sensoryInput1);
      setMotorInput1(data.motorInput1);

      setArea1(data.potentials.area1);
      setArea2(data.potentials.area2);
      setArea3(data.potentials.area3);
      setArea4(data.potentials.area4);
      setArea5(data.potentials.area5);
      setArea6(data.potentials.area6);
    };

    const onErrorNotification = (data: { msg: string }) => {
      setErrorNotification({ show: true, msg: data.msg });

      // Hide the toast after 3 seconds
      setTimeout(() => {
        setErrorNotification({ show: false, msg: '' });
      }, 3000);
    };

    const onInfoNotification = (data: { msg: string }) => {
      setInfoNotification({ show: true, msg: data.msg });

      // Hide the toast after 3 seconds
      setTimeout(() => {
        setInfoNotification({ show: false, msg: '' });
      }, 3000);
    };

    socket.on(InboundEvent.Connect, onConnect);
    socket.on(InboundEvent.Disconnect, onDisconnect);
    socket.on(InboundEvent.NewActivity, onNewActivity);
    socket.on(InboundEvent.ErrorNotification, onErrorNotification);
    socket.on(InboundEvent.InfoNotification, onInfoNotification);

    return () => {
      socket.off(InboundEvent.Connect, onConnect);
      socket.off(InboundEvent.Disconnect, onDisconnect);
      socket.off(InboundEvent.NewActivity, onNewActivity);
      socket.off(InboundEvent.ErrorNotification, onErrorNotification);
      socket.off(InboundEvent.InfoNotification, onInfoNotification);
    };
  }, []);

  /**
   * @todo careful here
   * these values can be changed by the server during training
   * they can also be changed by the user in the GUI
   * beware of update loops: server -> new value -> update state -> render new state -> trigger on-change event -> emit update back to server
   */
  const handleNetworkTrainingActivatedChange = (newTrainNet: boolean) => {
    setNetworkTrainingActivated(newTrainNet);
    socket.emit(
      OutboundEvent.UpdateConfig,
      'network-training-activated',
      newTrainNet,
    );
  };

  const handlePatternNumberChange = (newPatternNumber: number) => {
    setPatternNumber(newPatternNumber);
    socket.emit(OutboundEvent.UpdateConfig, 'pattern-number', newPatternNumber);
  };

  return (
    <div className="App">
      <TransientToast
        show={errorNotification.show}
        error={true}
        msg={errorNotification.msg}
        onClose={() => setErrorNotification({ show: false, msg: '' })}
      />
      <TransientToast
        show={infoNotification.show}
        error={false}
        msg={infoNotification.msg}
        onClose={() => setInfoNotification({ show: false, msg: '' })}
      />
      <ControlPanel
        visible={true}
        connectedToServer={connected}
        currentSimulationStep={currentStep}
        patternNumber={patternNumber}
        setPatternNumber={setPatternNumber}
        onPatternNumberChange={handlePatternNumberChange}
        networkTrainingActivated={networkTrainingActivated}
        onNetworkTrainingActivatedChange={handleNetworkTrainingActivatedChange}
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
          <Totals
            totalActivity={totalActivity}
            globalInhibition={globalInhibition}
          />
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
