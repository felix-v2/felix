/* eslint-disable react/prop-types */
import { Dispatch, createContext, useContext, useReducer } from 'react';

export interface Parameters {
    io: number;
    noise: number;
    steps: number;
    displaySteps: number;
    sensoryInputRow: number;
    sensoryInputCol: number;
    motorInputRow: number;
    motorInputCol: number;
    gain: number;
    theta: number;
    sensoryStimAmp: number;
    motorStimAmp: number;
    pattern: number;
    learn: number;
    diluteProb: number;
    diluteArea: number;
    jFfb: number;
    jRec: number;
    jInh: number;
    jSlow: number;
    hasSensoryInput: boolean;
    hasMotorInput: boolean;
    hasDilute: boolean;
    hasSaveNet: boolean;
    hasLoadNet: boolean;
    hasTrainNet: boolean;
    hasPrintNet: boolean;
    hasComputeCA: boolean;
}

const defaultParameters: Parameters = {
    io: 0,
    noise: 0,
    steps: 0,
    displaySteps: 0,
    sensoryInputRow: 0,
    sensoryInputCol: 0,
    sensoryStimAmp: 0,
    motorInputCol: 0,
    motorInputRow: 0,
    gain: 0,
    theta: 0,
    pattern: 0,
    learn: 0,
    diluteArea: 0,
    diluteProb: 0,
    jFfb: 0,
    jRec: 0,
    jInh: 0,
    jSlow: 0,
    motorStimAmp: 0,
    hasSensoryInput: false,
    hasMotorInput: false,
    hasDilute: false,
    hasComputeCA: false,
    hasLoadNet: false,
    hasPrintNet: false,
    hasSaveNet: false,
    hasTrainNet: false,
};

const ParametersContext = createContext<
    | {
          parameters: Parameters;
          dispatch: Dispatch<Record<string, number | boolean>>;
      }
    | undefined
>(undefined);

const ParametersReducer = (
    state: Parameters,
    action: Record<string, number | boolean>
) => {
    return { ...state, ...action };
};

export const ParametersProvider: React.FC<{ children: React.ReactNode }> = ({
    children,
}) => {
    const [parameters, dispatch] = useReducer(
        ParametersReducer,
        defaultParameters
    );

    return (
        <ParametersContext.Provider value={{ parameters, dispatch }}>
            {children}
        </ParametersContext.Provider>
    );
};

export const useParameters = () => {
    const context = useContext(ParametersContext);

    if (context === undefined) {
        throw new Error(
            'useParameters must be used within a ParametersProvider'
        );
    }

    return context;
};
