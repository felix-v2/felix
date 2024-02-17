import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np


# Note: very brut-ish and ugly unit tests but they will do for now to ensure the code works as expected
class TestStandardNet6Areas(unittest.TestCase):

    @staticmethod
    def assertZeroActivity(arr: np.array, els: int):
        """
        Testing util func: asserts the 1d array with {els} elements, all with zero values.
        Aka an initialised empty vector (after main_init, but before simulation has started)
        """
        np.testing.assert_array_equal(arr, np.zeros(els))

    def assertNonZeroActivity(self, arr: np.array):
        """
        Testing util func: asserts the array has some non-zero values.
        Aka an initialised non-empty vector (during simulation)
        """
        self.assertTrue(not np.all(arr == 0))

    def test_display_K(self):
        net = StandardNet6Areas()
        self.assertEqual(net.display_K(), {
            1: [1, 2],
            2: [1, 2, 3],
            3: [2, 3, 4],
            4: [3, 4, 5],
            5: [4, 5, 6],
            6: [5, 6]
        })

    def test_main_init(self):
        net = StandardNet6Areas()
        net.main_init()

        self.assertZeroActivity(net.pot, net.NAREAS * net.N1)
        self.assertZeroActivity(net.rates, net.NAREAS * net.N1)
        self.assertZeroActivity(net.inh, net.NAREAS * net.N1)
        self.assertZeroActivity(net.avg_patts, net.NAREAS * net.N1 * net.P)
        self.assertZeroActivity(net.ca_patts, net.NAREAS * net.N1 * net.P)
        self.assertZeroActivity(net.ca_ovlps, net.NAREAS * net.P * net.P)
        self.assertZeroActivity(net.ovlps, net.NAREAS * net.P)
        self.assertZeroActivity(net.slowinh, net.NAREAS)
        self.assertZeroActivity(net.adapt, net.NAREAS * net.N1)
        self.assertZeroActivity(net.diluted, net.NAREAS * net.N1)
        self.assertZeroActivity(net.above_thresh, net.NAREAS * net.N1)
        self.assertZeroActivity(net.above_hstory, net.NAREAS * net.N1 * net.P)
        self.assertZeroActivity(net.tot_LTP, net.NAREAS)
        self.assertZeroActivity(net.tot_LTD, net.NAREAS)
        self.assertZeroActivity(net.sensInput, net.NYAREAS * net.N1)
        self.assertZeroActivity(net.motorInput, net.NYAREAS * net.N1)
        self.assertZeroActivity(net.sensPatt, net.NYAREAS*net.P*net.N1)
        self.assertZeroActivity(net.motorPatt, net.NYAREAS*net.P*net.N1)
        self.assertZeroActivity(net.J, net.NAREAS * net.NAREAS * net.NSQR1)
        self.assertZeroActivity(net.Jinh, net.N1)
        self.assertZeroActivity(net.linkffb, net.N1)
        self.assertZeroActivity(net.linkrec, net.N1)
        self.assertZeroActivity(net.linkinh, net.N1)
        self.assertZeroActivity(net.tempffb, net.N1)
        self.assertZeroActivity(net.clampSMIn, net.N1)

    def test_resetNet(self):
        net = StandardNet6Areas()
        net.main_init()

        # make sure there is non-zero activity in the network
        net.randomise_net_activity()

        self.assertNonZeroActivity(net.pot)
        self.assertNonZeroActivity(net.inh)
        self.assertNonZeroActivity(net.adapt)
        self.assertNonZeroActivity(net.rates)
        self.assertNonZeroActivity(net.slowinh)
        self.assertNonZeroActivity(net.tot_LTP)
        self.assertNonZeroActivity(net.tot_LTD)
        self.assertNonZeroActivity(net.above_hstory)
        self.assertTrue(net.total_output > 0)

        # then check that the reset zeroes all activity
        net.resetNet()

        self.assertZeroActivity(net.pot, net.NAREAS * net.N1)
        self.assertZeroActivity(net.inh, net.NAREAS * net.N1)
        self.assertZeroActivity(net.adapt, net.NAREAS * net.N1)
        self.assertZeroActivity(net.rates, net.NAREAS * net.N1)
        self.assertZeroActivity(net.slowinh, net.NAREAS)
        self.assertZeroActivity(net.tot_LTP, net.NAREAS)
        self.assertZeroActivity(net.tot_LTD, net.NAREAS)
        self.assertZeroActivity(
            net.above_hstory, net.NAREAS * net.N1 * net.P)
        self.assertEqual(net.total_output, 0.0)

if __name__ == "__main__":
    unittest.main()
