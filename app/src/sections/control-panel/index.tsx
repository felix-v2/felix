import { useEffect, useState } from 'react';
import {
  Button,
  ButtonGroup,
  Card,
  Col,
  Offcanvas,
  ProgressBar,
  Row,
  ToggleButton,
} from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Slider } from '../../components/slider';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';

import { OutboundEvent, socket } from '../../socket';

export const ControlPanel = ({
  onHide,
  connectedToServer,
  currentSimulationStep,
  patternNumber,
  setPatternNumber,
  onPatternNumberChange,
  networkTrainingActivated,
  onNetworkTrainingActivatedChange,
  computeCaOverlaps,
  onComputeCaOverlapsChange,
}: {
  visible: boolean;
  onHide: () => void;
  connectedToServer: boolean;
  currentSimulationStep: number;
  patternNumber: number;
  setPatternNumber: (patternNumber: number) => void;
  onPatternNumberChange: (patternNumber: number) => void;
  networkTrainingActivated: boolean;
  onNetworkTrainingActivatedChange: (newTrainNet: boolean) => void;
  computeCaOverlaps: boolean;
  onComputeCaOverlapsChange: (newComputeCaOverlaps: boolean) => void;
}) => {
  const connectToServer = () => {
    socket.connect();
  };

  return (
    <Offcanvas
      show={true}
      onHide={onHide}
      placement="end"
      scroll={true}
      backdrop={false}
      style={{
        backgroundColor: '#e2e3e5',
        transform: 'none',
      }}
    >
      <Offcanvas.Header style={{ paddingTop: 30 }}>
        <Col xs={4}>
          <Offcanvas.Title>Felix</Offcanvas.Title>
        </Col>
        <Col xs={8}>
          <ProgressBar
            style={{ height: '2rem' }}
            animated
            variant={connectedToServer ? 'success' : 'danger'}
            now={100}
            label={
              connectedToServer
                ? `Simulation step: ${currentSimulationStep}`
                : 'Connect to server'
            }
            onClick={connectToServer}
          />
        </Col>
      </Offcanvas.Header>
      <Offcanvas.Body>
        <Row style={{ paddingTop: 20 }}>
          <Col xs={12}>
            <SimulationControlButtons connectedToServer={connectedToServer} />
          </Col>
        </Row>
        <Row style={{ paddingTop: 40 }}>
          <Col xs={12}>
            <SimulationSwitches
              networkTrainingActivated={networkTrainingActivated}
              onNetworkTrainingActivatedChange={
                onNetworkTrainingActivatedChange
              }
              computeCaOverlaps={computeCaOverlaps}
              onComputeCaOverlapsChange={onComputeCaOverlapsChange}
            />
          </Col>
        </Row>
        <Row style={{ paddingTop: 30 }}>
          <Col xs={12}>
            <SimulationModelParameters
              patternNumber={patternNumber}
              setPatternNumber={setPatternNumber}
              onPatternNumberChange={onPatternNumberChange}
            />
          </Col>
        </Row>
      </Offcanvas.Body>
    </Offcanvas>
  );
};

const SimulationControlButtons = ({
  connectedToServer,
}: {
  connectedToServer: boolean;
}) => {
  const initSimulation = () => {
    socket.emit(OutboundEvent.InitSimulation);
  };

  const continueSimulation = () => {
    socket.emit(OutboundEvent.ContinueSimulation);
  };

  return (
    <Card>
      <Card.Body>
        <Card.Title style={{ fontSize: '1rem' }}>Controls</Card.Title>
        <ButtonGroup size="sm" className="mb-2">
          <Button
            style={{ marginRight: 10 }}
            variant="light"
            onClick={initSimulation}
            disabled={!connectedToServer}
          >
            Init
          </Button>
          <Button
            style={{ marginRight: 10 }}
            onClick={continueSimulation}
            disabled={!connectedToServer}
          >
            Continue
          </Button>
          <Button style={{ marginRight: 10 }} variant="info" disabled={true}>
            Steps
          </Button>
          <Button style={{ marginRight: 10 }} variant="danger" disabled={true}>
            Stop
          </Button>
          <Button style={{ marginRight: 10 }} variant="success" disabled={true}>
            Run
          </Button>
        </ButtonGroup>
      </Card.Body>
    </Card>
  );
};

const SimulationSwitches = ({
  networkTrainingActivated,
  onNetworkTrainingActivatedChange,
  computeCaOverlaps,
  onComputeCaOverlapsChange,
}: {
  networkTrainingActivated: boolean;
  onNetworkTrainingActivatedChange: (newTrainNet: boolean) => void;
  computeCaOverlaps: boolean;
  onComputeCaOverlapsChange: (newComputeCaOverlaps: boolean) => void;
}) => {
  const [sensIn, setSensIn] = useState<boolean>(false);
  const [motorIn, setMotorIn] = useState<boolean>(false);

  const handleSensInChange = () => {
    const newSensIn = !sensIn;
    setSensIn(newSensIn);

    socket.emit(
      OutboundEvent.UpdateConfig,
      'is-receiving-sensory-input',
      newSensIn,
    );
  };

  const handleMotorInChange = () => {
    const newMotorIn = !motorIn;
    setMotorIn(newMotorIn);

    socket.emit(
      OutboundEvent.UpdateConfig,
      'is-receiving-motor-input',
      newMotorIn,
    );
  };

  const handleUserChangeNetworkTrainingActivated = () => {
    onNetworkTrainingActivatedChange(!networkTrainingActivated);
  };

  const handleUserChangeComputeCaOverlaps = () => {
    onComputeCaOverlapsChange(!computeCaOverlaps);
  };

  return (
    <>
      <Card>
        <Card.Body>
          <Card.Title style={{ fontSize: '1rem' }}>Switches</Card.Title>
          <ButtonGroup size="sm" className="mb-2">
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-sensIn"
              type="checkbox"
              checked={sensIn}
              value={sensIn.toString()} // required string/number, but doesn't impact the functionality directly
              onChange={handleSensInChange}
            >
              sensIn
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-motorIn"
              type="checkbox"
              checked={motorIn}
              value={motorIn.toString()}
              onChange={handleMotorInChange}
            >
              motorIn
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-dilute"
              value={'dilute'}
              disabled={true}
            >
              dilute
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-saveNet"
              value={'saveNet'}
              disabled={true}
            >
              saveNet
            </ToggleButton>
          </ButtonGroup>
          <ButtonGroup size="sm" className="mb-2">
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-loadNet"
              value={'loadNet'}
              disabled={true}
            >
              loadNet
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-trainNet"
              checked={networkTrainingActivated}
              value={networkTrainingActivated.toString()}
              onClick={handleUserChangeNetworkTrainingActivated}
            >
              trainNet
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-printNet"
              value={'printNet'}
              disabled={true}
            >
              printNet
            </ToggleButton>
          </ButtonGroup>
          <ButtonGroup size="sm" className="mb-2">
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-computeCA/Ovlps"
              checked={computeCaOverlaps}
              value={computeCaOverlaps.toString()}
              onClick={handleUserChangeComputeCaOverlaps}
            >
              computeCA/Ovlps
            </ToggleButton>
          </ButtonGroup>
        </Card.Body>
      </Card>
    </>
  );
};

const SimulationModelParameters = ({
  patternNumber,
  setPatternNumber,
  onPatternNumberChange,
}: {
  patternNumber: number;
  setPatternNumber: (patterNumber: number) => void;
  onPatternNumberChange: (patterNumber: number) => void;
}) => {
  const [io, setIo] = useState<number>(0);
  const [noise, setNoise] = useState<number>(5);
  const [steps, setSteps] = useState<number>(0);
  const [displaySteps, setDisplaySteps] = useState<number>(0);
  const [sensoryInputRow, setSensoryInputRow] = useState<number>(0);
  const [sensoryInputCol, setSensoryInputCol] = useState<number>(0);
  const [motorInputRow, setMotorInputRow] = useState<number>(0);
  const [motorInputCol, setMotorInputCol] = useState<number>(0);
  const [gain, setGain] = useState<number>(1000);
  const [theta, setTheta] = useState<number>(0);
  const [sensoryStimAmp, setSensoryStimAmp] = useState<number>(300);
  const [motorStimAmp, setMotorStimAmp] = useState<number>(300);
  const [learn, setLearn] = useState<number>(0);
  const [diluteProb, setDiluteProb] = useState<number>(0);
  const [diluteArea, setDiluteArea] = useState<number>(0);
  const [jFfb, setJffb] = useState<number>(500);
  const [jRec, setJRec] = useState<number>(500);
  const [jInh, setJInh] = useState<number>(500);
  const [jSlow, setJSlow] = useState<number>(60);

  const serverUpdateNoise = () => {
    socket.emit(OutboundEvent.UpdateConfig, 'noise', noise);
  };

  const serverUpdateGlobalInhibition = () => {
    socket.emit(OutboundEvent.UpdateConfig, 'global-inhibition', jSlow);
  };

  const serverUpdateSensoryStimulationAmplitude = () => {
    socket.emit(
      OutboundEvent.UpdateConfig,
      'sensory-stimulation-amplitude',
      sensoryStimAmp,
    );
  };

  const serverUpdateMotorStimulationAmplitude = () => {
    socket.emit(
      OutboundEvent.UpdateConfig,
      'motor-stimulation-amplitude',
      motorStimAmp,
    );
  };

  const handleUserChangePatternNumber = (patternNumber: number) => {
    onPatternNumberChange(patternNumber);
  };

  return (
    <>
      <Card style={{ fontSize: '0.8rem' }}>
        <Card.Body>
          <Card.Title style={{ fontSize: '1rem' }}>Parameters</Card.Title>
          <Row>
            <Col xs={6}></Col>
            <Col xs={6}></Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="IO"
                min={-1000}
                max={1000}
                value={io}
                setValue={setIo}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Noise"
                min={0}
                max={1000}
                value={noise}
                setValue={setNoise}
                onAfterChange={serverUpdateNoise}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Display steps"
                min={1}
                max={100}
                value={displaySteps}
                setValue={setDisplaySteps}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Steps"
                min={1}
                max={100}
                value={steps}
                setValue={setSteps}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Motor input row"
                min={1}
                max={2}
                value={motorInputRow}
                setValue={setMotorInputRow}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Motor input col"
                min={1}
                max={6}
                value={motorInputCol}
                setValue={setMotorInputCol}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Sensory input row"
                min={1}
                max={2}
                value={sensoryInputRow}
                setValue={setSensoryInputRow}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Sensory input col"
                min={1}
                max={3}
                value={sensoryInputCol}
                setValue={setSensoryInputCol}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Jffb"
                min={0}
                max={5000}
                value={jFfb}
                setValue={setJffb}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Jrec"
                min={0}
                max={5000}
                value={jRec}
                setValue={setJRec}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Gain"
                min={0}
                max={5000}
                value={gain}
                setValue={setGain}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Theta"
                min={0}
                max={5000}
                value={theta}
                setValue={setTheta}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Sensory stim. amp"
                min={0}
                max={1000}
                value={sensoryStimAmp}
                setValue={setSensoryStimAmp}
                onAfterChange={serverUpdateSensoryStimulationAmplitude}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Motor stim. amp"
                min={0}
                max={1000}
                value={motorStimAmp}
                setValue={setMotorStimAmp}
                onAfterChange={serverUpdateMotorStimulationAmplitude}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Jinh"
                min={0}
                max={5000}
                value={jInh}
                setValue={setJInh}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Pattern #"
                min={0}
                max={13}
                value={patternNumber}
                setValue={setPatternNumber}
                onAfterChange={(e) =>
                  handleUserChangePatternNumber(Number(e.target.value))
                }
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Learn"
                min={0}
                max={1000}
                value={learn}
                setValue={setLearn}
              ></Slider>
            </Col>
            <Col xs={6}>
              {' '}
              <Slider
                title="Dilute prob"
                min={0}
                max={100}
                value={diluteProb}
                setValue={setDiluteProb}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Dilute area"
                min={0}
                max={6}
                value={diluteArea}
                setValue={setDiluteArea}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="J-slow"
                min={0}
                max={5000}
                value={jSlow}
                setValue={setJSlow}
                onAfterChange={serverUpdateGlobalInhibition}
              ></Slider>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </>
  );
};
