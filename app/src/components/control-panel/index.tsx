import { useState } from 'react';
import { Col, Offcanvas, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Slider } from './slider';

export const ControlPanel = ({
  visible,
  onHide,
}: {
  visible: boolean;
  onHide: () => void;
}) => {
  // sliders
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
          <Col xs={3}>
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
          <Col xs={3}>
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
          <Col xs={3}>
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
          <Col xs={3}>
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
