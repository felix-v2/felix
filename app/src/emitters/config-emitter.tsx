import { useEffect } from 'react';
import { useParameters } from '../providers/parameters-provider';
import { Socket } from 'socket.io-client';
import { Events } from '../listeners/events.enum';

export const ConfigEmitter: React.FC<{ socket: Socket }> = ({ socket }) => {
    const {
        parameters: { hasSensoryInput, hasMotorInput },
    } = useParameters();

    useEffect(() => {
        console.log('input change');
        socket.emit(Events.UPDATE_CONFIG, {
            hasMotorInput,
            hasSensoryInput,
        });
    }, [hasMotorInput, hasSensoryInput, socket]);

    return null;
};
