import { io } from 'socket.io-client';
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import { ParametersProvider } from './providers/parameters-provider';
import { NewActivityListener } from './listeners/new-activity-listener';
import { PotentialsProvider } from './providers/potentials-provider';
import { ConfigEmitter } from './emitters/config-emitter';
import { SimulationEmitter } from './emitters/simulation-emitter';
import { ApplicationContainer } from './sections/application-container';
import { SimulationStatusProvider } from './providers/simulation-status-provider';

const socket = io('ws://localhost:5000', { autoConnect: true });

/**
 * @todo Refactor state into objects, use Zod schemas, validate in websocket handlers, and declare state locally
 * @todo Refactor socket-io interface https://socket.io/how-to/use-with-react
 * @todo Responsivity?
 */
export default function App() {

  return (
    <div className="App">
      <ParametersProvider>
        <PotentialsProvider>
          <SimulationStatusProvider>
            <NewActivityListener socket={socket} />
            <ConfigEmitter socket={socket} />
            <SimulationEmitter socket={socket} />
            <ApplicationContainer />  
          </SimulationStatusProvider>
        </PotentialsProvider>
      </ParametersProvider>
    </div>
  );
}
