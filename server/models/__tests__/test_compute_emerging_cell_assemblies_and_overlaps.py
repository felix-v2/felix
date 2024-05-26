import unittest
from ..standardNet6Areas import StandardNet6Areas
import numpy as np


class TestComputeEmergingCellAssembliesAndOverlaps(unittest.TestCase):
    def test_compute_emerging_cell_assemblies_and_overlaps(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_ca_patts = net.ca_patts.copy()
        start_ca_ovlps = net.ca_ovlps.copy()

        net.sCA_ovlps = True

        net.compute_emerging_cell_assemblies_and_overlaps()

        self.assertFalse(np.allclose(net.ca_patts, start_ca_patts))
        self.assertFalse(np.allclose(net.ca_ovlps, start_ca_ovlps))
        self.assertFalse(net.sCA_ovlps)

    def test_does_not_compute_if_flag_is_false(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_ca_patts = net.ca_patts.copy()
        start_ca_ovlps = net.ca_ovlps.copy()

        net.sCA_ovlps = False

        net.compute_emerging_cell_assemblies_and_overlaps()

        self.assertTrue(np.allclose(net.ca_patts, start_ca_patts))
        self.assertTrue(np.allclose(net.ca_ovlps, start_ca_ovlps))
        self.assertFalse(net.sCA_ovlps)


if __name__ == "__main__":
    unittest.main()
