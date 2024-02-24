import { Accordion, Col, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Heatmap } from '../graphs/heatmap';

export const Potentials = ({
  sensoryInput1,
  area1,
  area2,
  area3,
  area4,
  area5,
  area6,
  motorInput1,
}: {
  sensoryInput1: number[][];
  area1: number[][];
  area2: number[][];
  area3: number[][];
  area4: number[][];
  area5: number[][];
  area6: number[][];
  motorInput1: number[][];
}) => {
  return (
    <Accordion
      defaultActiveKey="0"
      style={{
        marginLeft: 'auto',
        marginRight: 'auto',
      }}
    >
      <Accordion.Item eventKey="0">
        <Accordion.Header style={{ fontSize: '1rem' }}>
          Potentials
        </Accordion.Header>
        <Accordion.Body style={{ paddingTop: 10, paddingBottom: 10 }}>
          <Row>
            <Col>
              {Heatmap({
                title: 'Sensory Input 1',
                activity: sensoryInput1,
                height: 130,
              })}
            </Col>
            <Col>
              {Heatmap({ title: 'Area 1', activity: area1, height: 130 })}
            </Col>
            <Col>
              {Heatmap({ title: 'Area 2', activity: area2, height: 130 })}
            </Col>
            <Col>
              {Heatmap({ title: 'Area 3', activity: area3, height: 130 })}
            </Col>
            <Col>
              {Heatmap({ title: 'Area 4', activity: area4, height: 130 })}
            </Col>
            <Col>
              {Heatmap({ title: 'Area 5', activity: area5, height: 130 })}
            </Col>
            <Col>
              {Heatmap({ title: 'Area 6', activity: area6, height: 130 })}
            </Col>
            <Col>
              {Heatmap({
                title: 'Motor Input 1',
                activity: motorInput1,
                height: 130,
              })}
            </Col>
          </Row>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
};
