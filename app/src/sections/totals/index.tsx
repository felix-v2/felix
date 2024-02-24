import { Accordion, Col, Row } from 'react-bootstrap';
import { TimeSeriesGraph } from '../../components/graphs/line';

export const Totals = () => {
  return (
    <>
      <Row>
        <Col xs={3}>
          <CollapsibleTimeSeries title="Total network" />
        </Col>
        <Col xs={3}>
          <CollapsibleTimeSeries title="Slow Inhb" />
        </Col>
        <Col xs={3}>
          <CollapsibleTimeSeries title="LTP" />
        </Col>
        <Col xs={3}>
          <CollapsibleTimeSeries title="LTD" />
        </Col>
      </Row>
    </>
  );
};

export const CollapsibleTimeSeries = ({ title }: { title: string }) => {
  return (
    <>
      <Accordion defaultActiveKey="0">
        <Accordion.Item eventKey="0">
          <Accordion.Header>{title}</Accordion.Header>
          <Accordion.Body style={{ padding: 0 }}>
            <TimeSeriesGraph title={title} />
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
      ;
    </>
  );
};
