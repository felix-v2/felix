import { Accordion, Col, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Heatmap } from '../graphs/heatmap';

export const CellAssemblyPotentialsOverlaps = ({
  activity,
}: {
  activity: number[][];
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
        <Accordion.Header>Scalar(CA x Activity)</Accordion.Header>
        <Accordion.Body style={{ paddingTop: 10, paddingBottom: 10 }}>
          <Row>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A1',
                width: 130,
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A2',
                width: 130,
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A3',
                width: 130,
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A4',
                width: 130,
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A5',
                width: 130,
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A6',
                width: 130,
                activity: [],
              })}
            </Col>
          </Row>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
};
