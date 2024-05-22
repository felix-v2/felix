import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np


class TestComputeLearning(unittest.TestCase):
    def test_compute_learning(self):
        net = StandardNet6Areas()
        net.main_init()
        net.init()
        net.MAIN_INIT_RANDOM_ACTIVITY()

        # the func modifies the np slice in place, so use copy() so we can compare before and after
        start_rates = net.rates.copy()
        start_pot = net.pot.copy()
        start_j = net.J.copy()

        net.compute_learning(0.1)

        # each of the 6 (area) values in tot_LTP and tot_LTD updated
        self.assertEqual(np.count_nonzero(net.tot_LTP == 0), 0)
        self.assertEqual(np.count_nonzero(net.tot_LTD == 0), 0)

        # J updated
        self.assertFalse(np.allclose(net.J, start_j))

        # rates and pot unaffected
        self.assertTrue(np.allclose(net.rates, start_rates))
        self.assertTrue(np.allclose(net.pot, start_pot))


if __name__ == "__main__":
    unittest.main()
