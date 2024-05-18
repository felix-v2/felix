import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np


class TestComputeOverlapBetweenCellAssembliesAndCurrentActivity(unittest.TestCase):
    @staticmethod
    def assertSilentVector(arr: np.array, n: int):
        """
        Testing util func: asserts the 1d array with {els} elements, all with zero values.
        Aka an initialised empty vector (after main_init, but before simulation has started)
        """
        np.testing.assert_array_equal(arr, np.zeros(n))

    def test_compute_overlap_between_cell_assemblies_and_current_activity(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_rates = net.rates.copy()
        start_ca_patts = net.ca_patts.copy()
        start_ovlps = net.ovlps.copy()

        net.compute_overlap_between_cell_assemblies_and_current_activity()

        # check rates and ca_patts unchanged, but ovlps updated
        self.assertTrue(np.allclose(net.rates, start_rates))
        self.assertTrue(np.allclose(net.ca_patts, start_ca_patts))
        self.assertFalse(np.allclose(net.ovlps, start_ovlps))


if __name__ == "__main__":
    unittest.main()
