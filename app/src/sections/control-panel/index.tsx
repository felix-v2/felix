import { useState } from 'react';
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

export const ControlPanel = ({
  visible,
  onHide,
}: {
  visible: boolean;
  onHide: () => void;
}) => {
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
            variant={'success'}
            now={100}
            label={'Simulation in progress'}
          />
        </Col>
      </Offcanvas.Header>
      <Offcanvas.Body>
        <Row style={{ paddingTop: 20 }}>
          <Col xs={12}>
            <SimulationControlButtons />
          </Col>
        </Row>
        <Row style={{ paddingTop: 40 }}>
          <Col xs={12}>
            <SimulationSwitches />
          </Col>
        </Row>
        <Row style={{ paddingTop: 30 }}>
          <Col xs={12}>
            <SimulationModelParameters />
          </Col>
        </Row>
      </Offcanvas.Body>
    </Offcanvas>
  );
};

const SimulationControlButtons = () => {
  return (
    <Card>
      <Card.Body>
        <Card.Title style={{ fontSize: '1rem' }}>Controls</Card.Title>
        <ButtonGroup size="sm" className="mb-2">
          <Button style={{ marginRight: 10 }} variant="light">
            Init
          </Button>
          <Button style={{ marginRight: 10 }} variant="danger">
            Stop
          </Button>
          <Button style={{ marginRight: 10 }} variant="info">
            Steps
          </Button>
          <Button style={{ marginRight: 10 }}>Continue</Button>
          <Button style={{ marginRight: 10 }} variant="success">
            Run
          </Button>
        </ButtonGroup>
      </Card.Body>
    </Card>
  );
};

const SimulationSwitches = () => {
  return (
    <>
      <Card>
        <Card.Body>
          <Card.Title style={{ fontSize: '1rem' }}>Switches</Card.Title>
          <ButtonGroup size="sm" className="mb-2">
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              value={1}
            >
              sensIn
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-2"
              value={1}
            >
              motorIn
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              value={1}
            >
              dilute
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              value={1}
            >
              saveNet
            </ToggleButton>
          </ButtonGroup>
          <ButtonGroup size="sm" className="mb-2">
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              value={1}
            >
              loadNet
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-2"
              value={1}
            >
              trainNet
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              value={1}
            >
              printNet
            </ToggleButton>
          </ButtonGroup>
          <ButtonGroup size="sm" className="mb-2">
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              value={1}
            >
              computeCA/Ovlps
            </ToggleButton>
          </ButtonGroup>
        </Card.Body>
      </Card>
    </>
  );
};

const SimulationModelParameters = () => {
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
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Motor stim. amp"
                min={0}
                max={1000}
                value={motorStimAmp}
                setValue={setMotorStimAmp}
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
                value={pattern}
                setValue={setPattern}
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
              ></Slider>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </>
  );
};
