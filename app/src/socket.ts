import { io } from 'socket.io-client';

export const socket = io('ws://localhost:5000', { autoConnect: false });

export enum InboundEvent {
  Connect = 'connect',
  Disconnect = 'disconnect',
  NewActivity = 'new-activity',
}

export enum OutboundEvent {
  InitSimulation = 'init-simulation',
  ContinueSimulation = 'continue-simulation',
  UpdateNoise = 'update-noise',
}
