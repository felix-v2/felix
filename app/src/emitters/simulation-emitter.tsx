import { useEffect } from 'react';
import { useParameters } from '../providers/parameters-provider';
import { Socket } from 'socket.io-client';
import { useSimulationStatus } from '../providers/simulation-status-provider';
import { Events } from '../listeners/events.enum';

export const SimulationEmitter: React.FC<{ socket: Socket }> = ({ socket }) => {
    const {
        parameters: { hasSensoryInput, hasMotorInput },
    } = useParameters();
    const {
        simulationStatus: { connected, running },
        dispatch,
    } = useSimulationStatus();

    useEffect(() => {
        dispatch({ connected: socket.connected });

        if (running) {
            socket.emit(Events.START_SIMULATION, {
                hasMotorInput,
                hasSensoryInput,
            });
        }

        if (connected && !running) {
            socket.emit(Events.STOP_SIMULATION);
            // socket.disconnect();
            // socket.connect();
        }
    }, [socket, running, connected, hasMotorInput, hasSensoryInput, dispatch]);

    return null;
};
