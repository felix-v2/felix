import { Col, Row } from 'react-bootstrap';
import { CellAssembly } from './cell-assembly';
import { CellAssemblyOverlaps } from './cell-assembly-overlaps';
import { CellAssemblyPotentialsOverlaps } from './cell-assembly-potentials-overlaps';
import { ControlPanel } from './control-panel';
import { Potentials } from './potentials';
import { Totals } from './totals';
import { usePotentials } from '../providers/potentials-provider';

export const ApplicationContainer: React.FC = () => {
    const {
        potentials: {
            sensoryInput1,
            area1,
            area2,
            area3,
            area4,
            area5,
            area6,
            motorInput1,
        },
    } = usePotentials();

    return (
        <>
            <ControlPanel visible={true} onHide={() => console.log('Hide')} />
            <Col xs={10} style={{ marginTop: '40px' }}>
                <Row
                    style={{
                        marginBottom: '50px',
                        marginLeft: '5px',
                        marginRight: '100px',
                    }}
                >
                    <Col xs={6}>
                        <CellAssembly
                            name={'CA #1'}
                            activity={[]}
                        ></CellAssembly>
                    </Col>
                    <Col xs={6}>
                        <CellAssembly
                            name={'CA #2'}
                            activity={[]}
                        ></CellAssembly>
                    </Col>
                </Row>
                <Row
                    style={{
                        marginBottom: '50px',
                        marginLeft: '5px',
                        marginRight: '100px',
                    }}
                >
                    <Col xs={12}>
                        <Potentials
                            sensoryInput1={sensoryInput1}
                            area1={area1}
                            area2={area2}
                            area3={area3}
                            area4={area4}
                            area5={area5}
                            area6={area6}
                            motorInput1={motorInput1}
                        />
                    </Col>
                </Row>
                <Row
                    style={{
                        marginBottom: '50px',
                        marginLeft: '5px',
                        marginRight: '100px',
                    }}
                >
                    <Totals />
                </Row>
                <Row
                    style={{
                        marginBottom: '50px',
                        marginLeft: '5px',
                        marginRight: '100px',
                    }}
                >
                    <Col xs={6}>
                        <CellAssemblyOverlaps
                            activity={[]}
                        ></CellAssemblyOverlaps>
                    </Col>
                </Row>
                <Row
                    style={{
                        marginBottom: '50px',
                        marginLeft: '5px',
                        marginRight: '100px',
                    }}
                >
                    <Col xs={8}>
                        <CellAssemblyPotentialsOverlaps
                            activity={[]}
                        ></CellAssemblyPotentialsOverlaps>
                    </Col>
                </Row>
            </Col>
        </>
    );
};
