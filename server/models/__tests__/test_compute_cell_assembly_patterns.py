import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np
import util


class TestComputeCellAssemblyPatterns(unittest.TestCase):
    def test_compute_cell_assembly_patterns(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_avg_patts = net.avg_patts.copy()
        start_ca_patts = net.ca_patts.copy()

        net.compute_CApatts(net.CA_THRESH)

        self.assertTrue(np.allclose(net.avg_patts, start_avg_patts))
        self.assertFalse(np.allclose(net.ca_patts, start_ca_patts))
        self.assertTrue(np.all(np.isin(net.ca_patts, [0, 1])))

    def test_no_strongly_responsive_cell(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_ca_patts = net.ca_patts.copy()

        # if firing rate of maximally responsive cell < min cellrate, then
        net.MIN_CELLRATE = 0.1
        v = util.Get_Vector(net.N1*net.NAREAS*net.P)
        v.fill(0.005)
        net.avg_patts = v
        start_avg_patts = net.avg_patts.copy()

        net.compute_CApatts(net.CA_THRESH)

        self.assertTrue(np.allclose(net.avg_patts, start_avg_patts))
        self.assertTrue(np.allclose(net.ca_patts, start_ca_patts))


if __name__ == "__main__":
    unittest.main()
