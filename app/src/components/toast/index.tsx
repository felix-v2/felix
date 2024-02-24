import React, { useState } from 'react';
import { ToastContainer } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Toast from 'react-bootstrap/Toast';

function TransientToast({ error }: { error: boolean } = { error: false }) {
  const [show, setShow] = useState(true);

  return (
    <ToastContainer position="top-start" style={{ padding: 50 }}>
      <Toast
        bg={error ? 'danger' : 'dark'}
        onClose={() => setShow(false)}
        show={show}
        delay={3000}
        autohide
      >
        <Toast.Header>
          <img src="holder.js/20x20?text=%20" className="rounded me-2" alt="" />
          <strong className="me-auto">Connection error</strong>
        </Toast.Header>
        <Toast.Body className="Dark">
          There was an issue connecting to the net.
        </Toast.Body>
      </Toast>
    </ToastContainer>
  );
}

export default TransientToast;
