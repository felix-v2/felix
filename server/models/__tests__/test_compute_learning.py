import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np


class TestComputeLearning(unittest.TestCase):
    def test_compute_learning(self):
        net = StandardNet6Areas()
        net.main_init()
        net.init()
        net.MAIN_INIT_RANDOM_ACTIVITY()
        net.slrate = 0.1  # learning only runs if slrate > 0

        # the func modifies the np slice in place, so use copy() so we can compare before and after
        start_rates = net.rates.copy()
        start_pot = net.pot.copy()
        start_j = net.J.copy()
        start_tot_ltd = net.tot_LTD.copy()
        start_tot_ltp = net.tot_LTP.copy()

        net.compute_learning(0.1)

        # each of the 6 (area) values in tot_LTP and tot_LTD have changed
        self.assertTrue(np.all(net.tot_LTP != start_tot_ltp))
        self.assertTrue(np.all(net.tot_LTD != start_tot_ltd))

        # J updated
        self.assertFalse(np.allclose(net.J, start_j))

        # rates and pot unaffected
        self.assertTrue(np.allclose(net.rates, start_rates))
        self.assertTrue(np.allclose(net.pot, start_pot))

    def test_no_learning(self):
        net = StandardNet6Areas()
        net.main_init()
        net.INIT_RANDOM_ACTIVITY()

        net.slrate = 0  # learning only runs if slrate > 0

        # the func modifies the np slice in place, so use copy() so we can compare before and after
        start_rates = net.rates.copy()
        start_pot = net.pot.copy()
        start_j = net.J.copy()

        self.assertTrue(np.all(net.tot_LTD == 0))
        self.assertTrue(np.all(net.tot_LTP == 0))

        net.compute_learning(0.1)

        # learning not computed because slrate is 0 - so nothing changes
        self.assertTrue(np.all(net.tot_LTD == 0))
        self.assertTrue(np.all(net.tot_LTP == 0))
        self.assertTrue(np.allclose(net.J, start_j))
        self.assertTrue(np.allclose(net.rates, start_rates))
        self.assertTrue(np.allclose(net.pot, start_pot))


if __name__ == "__main__":
    unittest.main()
