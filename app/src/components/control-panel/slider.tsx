import { Col, Form, Row } from 'react-bootstrap';
import RangeSlider from 'react-bootstrap-range-slider';

export const Slider = ({
  title,
  min,
  max,
  value,
  setValue,
}: {
  title: string;
  min: number;
  max: number;
  value: number;
  setValue: (v: number) => void;
}) => {
  return (
    <Form style={{ marginTop: '10px', marginRight: '0' }}>
      <Form.Group as={Row}>
        <Form.Label>{title}</Form.Label>
        <Col xs="12">
          <RangeSlider
            value={value}
            min={min}
            max={max}
            onChange={(e) => setValue(Number(e.target.value))}
            size="sm"
          />
        </Col>
        {/* <Col xs="4">
          <Form.Control
            size="sm"
            value={`${value} / ${max}`}
            disabled={false}
          />
        </Col> */}
      </Form.Group>
    </Form>
  );
};
