import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np


class TestComputeFiringRates(unittest.TestCase):
    def test_compute_firing_rates(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_pot = net.pot.copy()
        start_adapt = net.adapt.copy()
        start_rates = net.rates.copy()
        start_total_output = net.total_output

        net.compute_firing_rates(0.1, 0.2)

        # pot, adapt unchanged; rates, total_output updated
        self.assertTrue(np.allclose(net.pot, start_pot))
        self.assertTrue(np.allclose(net.adapt, start_adapt))
        self.assertFalse(np.allclose(net.rates, start_rates))
        self.assertTrue(net.total_output > start_total_output)


if __name__ == "__main__":
    unittest.main()
