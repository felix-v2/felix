import { Accordion, Col, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Heatmap } from '../../components/graphs/heatmap';

export const CellAssemblyOverlaps = ({
  area1,
  area2,
  area3,
  area4,
  area5,
  area6,
}: {
  area1: number[][];
  area2: number[][];
  area3: number[][];
  area4: number[][];
  area5: number[][];
  area6: number[][];
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
        <Accordion.Header>Between-CAs overlaps</Accordion.Header>
        <Accordion.Body style={{ paddingTop: 10, paddingBottom: 10 }}>
          <Row>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              A1
              {Heatmap({
                title: 'A1',
                activity: area1,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              A2
              {Heatmap({
                title: 'A2',
                activity: area2,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              A3
              {Heatmap({
                title: 'A3',
                activity: area3,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              A4
              {Heatmap({
                title: 'A4',
                activity: area4,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              A5
              {Heatmap({
                title: 'A5',
                activity: area5,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              A6
              {Heatmap({
                title: 'A6',
                activity: area6,
              })}
            </Col>
          </Row>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
};
