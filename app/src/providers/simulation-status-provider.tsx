/* eslint-disable react/prop-types */
import { Dispatch, createContext, useContext, useReducer } from 'react';

export interface SimulationStatus {
    connected: boolean;
    running: boolean;
}

const defaultSimulationStatus = {
    connected: false,
    running: false,
};

const SimulationStatusContext = createContext<
    | {
          simulationStatus: SimulationStatus;
          dispatch: Dispatch<Record<string, boolean>>;
      }
    | undefined
>(undefined);

const SimulationStatusReducer = (
    state: SimulationStatus,
    action: Record<string, boolean>
) => {
    return { ...state, ...action };
};

export const SimulationStatusProvider: React.FC<{
    children: React.ReactNode;
}> = ({ children }) => {
    const [simulationStatus, dispatch] = useReducer(
        SimulationStatusReducer,
        defaultSimulationStatus
    );

    return (
        <SimulationStatusContext.Provider
            value={{ simulationStatus, dispatch }}
        >
            {children}
        </SimulationStatusContext.Provider>
    );
};

export const useSimulationStatus = () => {
    const context = useContext(SimulationStatusContext);

    if (context === undefined) {
        throw new Error(
            'useSimulationStatus must be used within a SimulationStatusProvider'
        );
    }

    return context;
};
