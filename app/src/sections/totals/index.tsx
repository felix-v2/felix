import { Accordion, Col, Row } from 'react-bootstrap';
import { TimeSeriesGraph } from '../../components/graphs/line';

export const Totals = () => {
  return (
    <>
      <Accordion defaultActiveKey="0">
        <Accordion.Item eventKey="0">
          <Accordion.Header>Totals</Accordion.Header>
          <Accordion.Body style={{ paddingTop: 10, paddingBottom: 10 }}>
            <Row>
              <Col xs={3}>
                <TimeSeriesGraph title={'Total network'} />
              </Col>
              <Col xs={3}>
                <TimeSeriesGraph title={'Slow Inhb'} />
              </Col>
              <Col xs={3}>
                <TimeSeriesGraph title={'LTP'} />
              </Col>
              <Col xs={3}>
                <TimeSeriesGraph title={'LTD'} />
              </Col>
            </Row>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
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
          <Accordion.Header>{title}</Accordion.Header>
          <Accordion.Body style={{ paddingTop: 10, paddingBottom: 10 }}>
            {graph}
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
      ;
    </>
  );
};
