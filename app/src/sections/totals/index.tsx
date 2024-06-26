import { Accordion, Col, Row } from 'react-bootstrap';
import { TimeSeriesGraph } from '../../components/graphs/line';

export const Totals = ({
  totalActivity,
  globalInhibition,
  longTermPotentiation,
  longTermDepression,
}: {
  totalActivity: number[];
  globalInhibition: number[];
  longTermPotentiation: number[];
  longTermDepression: number[];
}) => {
  return (
    <>
      <Row>
        <Col xs={3}>
          <CollapsibleTimeSeries title="Total network" data={totalActivity} />
        </Col>
        <Col xs={3}>
          <CollapsibleTimeSeries title="Slow Inhb" data={globalInhibition} />
        </Col>
        <Col xs={3}>
          <CollapsibleTimeSeries title="LTP" data={longTermPotentiation} />
        </Col>
        <Col xs={3}>
          <CollapsibleTimeSeries title="LTD" data={longTermDepression} />
        </Col>
      </Row>
    </>
  );
};

export const CollapsibleTimeSeries = ({
  title,
  data,
}: {
  title: string;
  data: number[];
}) => {
  return (
    <>
      <Accordion defaultActiveKey="0">
        <Accordion.Item eventKey="0">
          <Accordion.Header>{title}</Accordion.Header>
          <Accordion.Body style={{ padding: 0 }}>
            <TimeSeriesGraph title={title} data={data} />
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
      ;
    </>
  );
};
