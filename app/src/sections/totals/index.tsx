import { Accordion, Col, Row } from 'react-bootstrap';
import { LineGraph } from '../../components/graphs/line';

export const Totals = () => {
  return (
    <>
      <Row>
        <Col xs={3}>
          <CollapsibleGraph
            title={'Total network'}
            graph={<LineGraph />}
          ></CollapsibleGraph>
        </Col>
        <Col xs={3}>
          <CollapsibleGraph
            title={'Slow inhib'}
            graph={<LineGraph />}
          ></CollapsibleGraph>
        </Col>
        <Col xs={3}>
          <CollapsibleGraph
            title={'LTP'}
            graph={<LineGraph />}
          ></CollapsibleGraph>
        </Col>
        <Col xs={3}>
          <CollapsibleGraph
            title={'LTD'}
            graph={<LineGraph />}
          ></CollapsibleGraph>
        </Col>
      </Row>
    </>
  );
};

const CollapsibleGraph = ({
  title,
  graph,
}: {
  title: string;
  graph: JSX.Element;
}) => {
  return (
    <>
      <Accordion defaultActiveKey="0">
        <Accordion.Item eventKey="0">
          <Accordion.Header style={{ fontSize: '1rem' }}>
            {title}
          </Accordion.Header>
          <Accordion.Body style={{ paddingTop: 10, paddingBottom: 10 }}>
            {graph}
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
      ;
    </>
  );
};
