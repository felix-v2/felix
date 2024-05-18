import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np
import util


class TestComputeNewAdaptation(unittest.TestCase):
    @staticmethod
    def assertSilentVector(arr: np.array, n: int):
        """
        Testing util func: asserts the 1d array with {els} elements, all with zero values.
        Aka an initialised empty vector (after main_init, but before simulation has started)
        """
        np.testing.assert_array_equal(arr, np.zeros(n))

    def test_compute_new_adaptation(self):
        net = StandardNet6Areas()
        net.main_init()
        net.INIT_RANDOM_ACTIVITY()

        start_rates = util.Get_Random_Vector(net.NAREAS * net.N1)
        start_adapt = util.Get_Random_Vector(net.NAREAS * net.N1)

        # set net.rates, net.adapt for each area
        # the func modifies the np slice in place, so use copy() so we can compare before and after
        net.rates = start_rates.copy()
        net.adapt = start_adapt.copy()
        net.compute_new_adaptation()

        self.assertTrue(np.allclose(net.rates, start_rates))  # rates unchanged
        self.assertFalse(np.allclose(net.adapt, start_adapt)
                         )  # adaptation updated


if __name__ == "__main__":
    unittest.main()
