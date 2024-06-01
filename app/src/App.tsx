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
  const [computeCaOverlaps, setComputeCaOverlaps] = useState<boolean>(false);

  // time-series data (1 area, 1d)
  const [totalActivity, setTotalActivity] = useState<number[]>([]);
  const [globalInhibition, setGlobalInhibition] = useState<number[]>([]);
  const [longTermPotentiation, setLongTermPotentiation] = useState<number[]>(
    [],
  );
  const [longTermDepression, setLongTermDepression] = useState<number[]>([]);

  // neural activity (1 area, 2d)
  const [sensoryInput1, setSensoryInput1] = useState<number[][]>(full);
  const [motorInput1, setMotorInput1] = useState<number[][]>(full);

  // neural activity (1 area, 2d)
  const [area1Potentials, setArea1Potentials] = useState<number[][]>(silence);
  const [area2Potentials, setArea2Potentials] = useState<number[][]>(silence);
  const [area3Potentials, setArea3Potentials] = useState<number[][]>(silence);
  const [area4Potentials, setArea4Potentials] = useState<number[][]>(silence);
  const [area5Potentials, setArea5Potentials] = useState<number[][]>(silence);
  const [area6Potentials, setArea6Potentials] = useState<number[][]>(silence);

  // cell assembly overlaps (6 areas, 2d - 12x12)
  const [area1CaOverlaps, setArea1CaOverlaps] = useState<number[][]>(silence);
  const [area2CaOverlaps, setArea2CaOverlaps] = useState<number[][]>(silence);
  const [area3CaOverlaps, setArea3CaOverlaps] = useState<number[][]>(silence);
  const [area4CaOverlaps, setArea4CaOverlaps] = useState<number[][]>(silence);
  const [area5CaOverlaps, setArea5CaOverlaps] = useState<number[][]>(silence);
  const [area6CaOverlaps, setArea6CaOverlaps] = useState<number[][]>(silence);

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
      setComputeCaOverlaps(data.config.computeCaOverlaps);

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

      setLongTermPotentiation((prevLongTermPotentiation) => {
        const updatedArray = [
          ...prevLongTermPotentiation,
          data.longTermPotentiation.area1,
        ];
        return updatedArray.length > 100 ? updatedArray.slice(1) : updatedArray;
      });

      setLongTermDepression((prevLongTermDepression) => {
        const updatedArray = [
          ...prevLongTermDepression,
          data.longTermDepression.area1,
        ];
        return updatedArray.length > 100 ? updatedArray.slice(1) : updatedArray;
      });

      setSensoryInput1(data.sensoryInput1);
      setMotorInput1(data.motorInput1);

      setArea1Potentials(data.potentials.area1);
      setArea2Potentials(data.potentials.area2);
      setArea3Potentials(data.potentials.area3);
      setArea4Potentials(data.potentials.area4);
      setArea5Potentials(data.potentials.area5);
      setArea6Potentials(data.potentials.area6);

      setArea1CaOverlaps(data.cellAssemblyOverlaps.area1);
      setArea2CaOverlaps(data.cellAssemblyOverlaps.area2);
      setArea3CaOverlaps(data.cellAssemblyOverlaps.area3);
      setArea4CaOverlaps(data.cellAssemblyOverlaps.area4);
      setArea5CaOverlaps(data.cellAssemblyOverlaps.area5);
      setArea6CaOverlaps(data.cellAssemblyOverlaps.area6);
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

  const handleComputeCaOverlapsChange = (newComputeCaOverlaps: boolean) => {
    setComputeCaOverlaps(newComputeCaOverlaps);
    socket.emit(
      OutboundEvent.UpdateConfig,
      'compute-ca-overlaps',
      newComputeCaOverlaps,
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
        computeCaOverlaps={computeCaOverlaps}
        onComputeCaOverlapsChange={handleComputeCaOverlapsChange}
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
              area1={area1Potentials}
              area2={area2Potentials}
              area3={area3Potentials}
              area4={area4Potentials}
              area5={area5Potentials}
              area6={area6Potentials}
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
            longTermPotentiation={longTermPotentiation}
            longTermDepression={longTermDepression}
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
            <CellAssemblyOverlaps
              area1={area1CaOverlaps}
              area2={area2CaOverlaps}
              area3={area3CaOverlaps}
              area4={area4CaOverlaps}
              area5={area5CaOverlaps}
              area6={area6CaOverlaps}
            ></CellAssemblyOverlaps>
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
