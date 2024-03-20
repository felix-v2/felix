/* eslint-disable react/prop-types */
import { Dispatch, createContext, useContext, useReducer } from 'react';
import { randActivity } from '../utils/rand-activity';

export interface Potentials {
    sensoryInput1: number[][];
    area1: number[][];
    area2: number[][];
    area3: number[][];
    area4: number[][];
    area5: number[][];
    area6: number[][];
    motorInput1: number[][];
}

const silence = randActivity({ silent: true });

const defaultPotentials = {
    sensoryInput1: silence,
    area1: silence,
    area2: silence,
    area3: silence,
    area4: silence,
    area5: silence,
    area6: silence,
    motorInput1: silence,
};

const PotentialsContext = createContext<
    | { potentials: Potentials; dispatch: Dispatch<Record<string, number>> }
    | undefined
>(undefined);

const PotentialsReducer = (
    state: Potentials,
    action: Record<string, number>
) => {
    return { ...state, ...action };
};

export const PotentialsProvider: React.FC<{ children: React.ReactNode }> = ({
    children,
}) => {
    const [potentials, dispatch] = useReducer(
        PotentialsReducer,
        defaultPotentials
    );

    return (
        <PotentialsContext.Provider value={{ potentials, dispatch }}>
            {children}
        </PotentialsContext.Provider>
    );
};

export const usePotentials = () => {
    const context = useContext(PotentialsContext);

    if (context === undefined) {
        throw new Error(
            'usePotentials must be used within a PotentialsProvider'
        );
    }

    return context;
};
