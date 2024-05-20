import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np


class TestComputeCellAssemblyOverlaps(unittest.TestCase):
    def test_compute_cell_assembly_overlaps(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_ca_patts = net.ca_patts.copy()
        start_ca_ovlps = net.ca_ovlps.copy()

        net.compute_CAoverlaps()

        self.assertTrue(np.allclose(net.ca_patts, start_ca_patts))
        self.assertFalse(np.allclose(net.ca_ovlps, start_ca_ovlps))


if __name__ == "__main__":
    unittest.main()
