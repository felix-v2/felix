import { useState } from 'react';
import { ToastContainer } from 'react-bootstrap';
import Toast from 'react-bootstrap/Toast';

function TransientToast(
  {
    show,
    error,
    msg,
    onClose,
  }: { show: boolean; error: boolean; msg: string; onClose: any } = {
    show: false,
    error: false,
    msg: '',
    onClose: () => {},
  },
) {
  return (
    <ToastContainer position="top-start" style={{ padding: 50 }}>
      <Toast
        bg={error ? 'danger' : 'success'}
        show={show}
        onClose={onClose}
        delay={3000}
        autohide
      >
        <Toast.Header>
          <img src="holder.js/20x20?text=%20" className="rounded me-2" alt="" />
          <strong className="me-auto">
            {error ? 'An error occurred.' : msg}
          </strong>
        </Toast.Header>
        <Toast.Body className="Dark">{error ? msg : ''}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
}

export default TransientToast;
