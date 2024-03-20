import { useEffect } from 'react';
import { Socket } from 'socket.io-client';
import { Events } from './events.enum';
import { usePotentials } from '../providers/potentials-provider';

export const NewActivityListener: React.FC<{ socket: Socket }> = ({
    socket,
}) => {
    const { dispatch } = usePotentials();

    useEffect(() => {
        socket.on(Events.NEW_ACTIVITY, (data) => {
            console.log('New activity received from server', {
                area1: data.area1,
            });
            dispatch({
                sensoryInput: data.sensoryInput1,
                area1: data.area1,
                area2: data.area2,
                area3: data.area3,
                area4: data.area4,
                area5: data.area5,
                area6: data.area6,
                motorInput1: data.motorInput1,
            });
        });
    }, [dispatch, socket]);

    return null;
};
