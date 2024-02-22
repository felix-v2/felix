import { Accordion, Col, Row } from 'react-bootstrap';

import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { Heatmap } from '../graphs/heatmap';

function generateArrayWithOnes(
  rows: number,
  columns: number,
  randomIndexes: number[],
  activity: number,
): number[][] {
  const withActivity: number[][] = Array.from({ length: rows }, () =>
    Array.from({ length: columns }, () => 0),
  );

  randomIndexes.forEach((index) => {
    withActivity[Math.floor(index / columns)][index % columns] = activity;
  });

  return withActivity;
}

const numIndexes = 19;
const randomIndexes = Array.from({ length: numIndexes }, () =>
  Math.floor(Math.random() * 25 * 25),
);

const inputAreas = generateArrayWithOnes(25, 25, randomIndexes, 0.7);
const otherAreas = generateArrayWithOnes(25, 25, randomIndexes, 0.03);

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
              {Heatmap({
                title: 'Area 1',
                activity: inputAreas,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'Area 2',
                activity: otherAreas,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'Area 3',
                activity: otherAreas,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'Area 4',
                activity: otherAreas,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'Area 5',
                activity: otherAreas,
              })}
            </Col>
            <Col style={{ paddingLeft: 0, paddingRight: 0 }}>
              {Heatmap({
                title: 'Area 6',
                activity: inputAreas,
              })}
            </Col>
          </Row>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
};
