import { Accordion, Col, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Heatmap } from '../graphs/heatmap/heatmap';

const generateRandomArray = (rows: number, columns: number): number[][] => {
  const randomArray: number[][] = [];

  for (let i = 0; i < rows; i++) {
    const row: number[] = [];
    for (let j = 0; j < columns; j++) {
      const value = i == j ? 0.8 : 0;
      row.push(value);
    }
    randomArray.push(row.reverse());
  }

  return randomArray;
};

export const CellAssemblyOverlaps = ({
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
        <Accordion.Header>Between-CAs overlaps</Accordion.Header>
        <Accordion.Body style={{ paddingTop: 10, paddingBottom: 10 }}>
          <Row>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A1',
                activity: generateRandomArray(12, 12),
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A2',
                activity: generateRandomArray(12, 12),
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A3',
                activity: generateRandomArray(12, 12),
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A4',
                activity: generateRandomArray(12, 12),
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A5',
                activity: generateRandomArray(12, 12),
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'A6',
                activity: generateRandomArray(12, 12),
              })}
            </Col>
          </Row>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
};
