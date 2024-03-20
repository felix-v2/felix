import {
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
import { useParameters } from '../../providers/parameters-provider';
import { useSimulationStatus } from '../../providers/simulation-status-provider';

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
  const { simulationStatus, dispatch } = useSimulationStatus();

  return (
    <Card>
      <Card.Body>
        <Card.Title style={{ fontSize: '1rem' }}>Controls</Card.Title>
        <ButtonGroup size="sm" className="mb-2">
          <ToggleButton style={{ marginRight: 10 }} variant="light" value={1} id='init'>
            Init
          </ToggleButton>
          <ToggleButton style={{ marginRight: 10 }} variant="danger" value={2} id='stop' checked={!simulationStatus.running}  onChange={(event) => dispatch({ running: !event.target.checked })} disabled={!simulationStatus.running}>
            Stop
          </ToggleButton>
          <ToggleButton style={{ marginRight: 10 }} variant="info" value={3} id='steps'>
            Steps
          </ToggleButton>
          <ToggleButton style={{ marginRight: 10 }} value={4} id='test'>Continue</ToggleButton>
          <ToggleButton style={{ marginRight: 10 }} variant="success" value={5} id='run' checked={!simulationStatus.running} onChange={(event) => dispatch({ running: event.target.checked })} disabled={simulationStatus.running}>
            Run
          </ToggleButton>
        </ButtonGroup>
      </Card.Body>
    </Card>
  );
};

const SimulationSwitches = () => {
  const { parameters, dispatch } = useParameters();

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
              checked={parameters.hasSensoryInput}
              value={1}
              onChange={(event) => dispatch({ hasSensoryInput: event.target.checked })}
            >
              sensIn
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-2"
              onChange={(event) => dispatch({ hasMotorInput: event.target.checked })}
              checked={parameters.hasMotorInput}
              value={2}
            >
              motorIn
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              checked={parameters.hasDilute}
              onChange={(event) => dispatch({ hasDilute: event.target.checked })}
              value={3}
            >
              dilute
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              checked={parameters.hasSaveNet}
              onChange={(event) => dispatch({ hasSaveNet: event.target.checked })}
              value={4}
            >
              saveNet
            </ToggleButton>
          </ButtonGroup>
          <ButtonGroup size="sm" className="mb-2">
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              onChange={(event) => dispatch({ hasLoadNet: event.target.checked })}
              checked={parameters.hasLoadNet}
              value={5}
            >
              loadNet
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-2"
              checked={parameters.hasTrainNet}
              onChange={(event) => dispatch({ hasTrainNet: event.target.checked })}
              value={6}
            >
              trainNet
            </ToggleButton>
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              checked={parameters.hasPrintNet}
              onChange={(event) => dispatch({ hasPrintNet: event.target.checked })}
              value={7}
            >
              printNet
            </ToggleButton>
          </ButtonGroup>
          <ButtonGroup size="sm" className="mb-2">
            <ToggleButton
              style={{ marginRight: 10 }}
              variant={'primary'}
              id="tbg-btn-1"
              checked={parameters.hasComputeCA}
              onChange={(event) => dispatch({ hasComputeCA: event.target.checked })}
              value={8}
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
  const { parameters, dispatch } = useParameters();

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
                value={parameters.io}
                setValue={(value) => dispatch({ io: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Noise"
                min={0}
                max={1000}
                value={parameters.noise}
                setValue={(value) => dispatch({ noise: value })}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Display steps"
                min={1}
                max={100}
                value={parameters.displaySteps}
                setValue={(value) => dispatch({ diplaySteps: value })}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Steps"
                min={1}
                max={100}
                value={parameters.steps}
                setValue={(value) => dispatch({ steps: value})}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Motor input row"
                min={1}
                max={2}
                value={parameters.motorInputRow}
                setValue={(value) => dispatch({ motorInputRow: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Motor input col"
                min={1}
                max={6}
                value={parameters.motorInputCol}
                setValue={(value) => dispatch({ motorInputCol: value})}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Sensory input row"
                min={1}
                max={2}
                value={parameters.sensoryInputRow}
                setValue={(value) => dispatch({ sensoryInputRow: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Sensory input col"
                min={1}
                max={3}
                value={parameters.sensoryInputCol}
                setValue={(value) => dispatch({ sensoryInputCol: value})}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Jffb"
                min={0}
                max={5000}
                value={parameters.jFfb}
                setValue={(value) => dispatch({ jFfb: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Jrec"
                min={0}
                max={5000}
                value={parameters.jRec}
                setValue={(value) => dispatch({ jRec: value})}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Gain"
                min={0}
                max={5000}
                value={parameters.gain}
                setValue={(value) => dispatch({ gain: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Theta"
                min={0}
                max={5000}
                value={parameters.theta}
                setValue={(value) => dispatch({ theta: value})}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Sensory stim. amp"
                min={0}
                max={1000}
                value={parameters.sensoryStimAmp}
                setValue={(value) => dispatch({ sensoryStimAmp: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Motor stim. amp"
                min={0}
                max={1000}
                value={parameters.motorStimAmp}
                setValue={(value) => dispatch({ motorStimAmp: value})}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Jinh"
                min={0}
                max={5000}
                value={parameters.jInh}
                setValue={(value) => dispatch({ jInh: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="Pattern #"
                min={0}
                max={13}
                value={parameters.pattern}
                setValue={(value) => dispatch({ pattern: value})}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Learn"
                min={0}
                max={1000}
                value={parameters.learn}
                setValue={(value) => dispatch({ learn: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              {' '}
              <Slider
                title="Dilute prob"
                min={0}
                max={100}
                value={parameters.diluteProb}
                setValue={(value) => dispatch({ diluteProb: value})}
              ></Slider>
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Slider
                title="Dilute area"
                min={0}
                max={6}
                value={parameters.diluteArea}
                setValue={(value) => dispatch({ diluteArea: value})}
              ></Slider>
            </Col>
            <Col xs={6}>
              <Slider
                title="J-slow"
                min={0}
                max={5000}
                value={parameters.jSlow}
                setValue={(value) => dispatch({ jSlow: value})}
              ></Slider>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </>
  );
};
