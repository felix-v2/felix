import { Accordion, Col, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Heatmap } from '../../components/graphs/heatmap';

export const CellAssembly = ({
  name,
  activity,
}: {
  name: string;
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
        <Accordion.Header>{name}</Accordion.Header>
        <Accordion.Body style={{ paddingTop: 10, paddingBottom: 10 }}>
          <Row>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              Area 1
              {Heatmap({
                title: 'Area 1',
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              Area 2
              {Heatmap({
                title: 'Area 2',
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              Area 3
              {Heatmap({
                title: 'Area 3',
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              Area 4
              {Heatmap({
                title: 'Area 4',
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              Area 5
              {Heatmap({
                title: 'Area 5',
                activity: [],
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              Area 6
              {Heatmap({
                title: 'Area 6',
                activity: [],
              })}
            </Col>
          </Row>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
};
