import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np
from unittest.mock import patch


class TestStandardNet6Areas(unittest.TestCase):

    @staticmethod
    def assertSilentVector(arr: np.array, n: int):
        """
        Testing util func: asserts the 1d array with {els} elements, all with zero values.
        Aka an initialised empty vector (after main_init, but before simulation has started)
        """
        np.testing.assert_array_equal(arr, np.zeros(n))

    def assertVectorWithActivity(self, arr: np.array):
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

        self.assertSilentVector(net.pot, net.NAREAS * net.N1)
        self.assertSilentVector(net.rates, net.NAREAS * net.N1)
        self.assertSilentVector(net.inh, net.NAREAS * net.N1)
        self.assertSilentVector(net.avg_patts, net.NAREAS * net.N1 * net.P)
        self.assertSilentVector(net.ca_patts, net.NAREAS * net.N1 * net.P)
        self.assertSilentVector(net.ca_ovlps, net.NAREAS * net.P * net.P)
        self.assertSilentVector(net.ovlps, net.NAREAS * net.P)
        self.assertSilentVector(net.slowinh, net.NAREAS)
        self.assertSilentVector(net.adapt, net.NAREAS * net.N1)
        self.assertSilentVector(net.diluted, net.NAREAS * net.N1)
        self.assertSilentVector(net.above_thresh, net.NAREAS * net.N1)
        self.assertSilentVector(net.above_hstory, net.NAREAS * net.N1 * net.P)
        self.assertSilentVector(net.tot_LTP, net.NAREAS)
        self.assertSilentVector(net.tot_LTD, net.NAREAS)
        self.assertSilentVector(net.sensInput, net.NYAREAS * net.N1)
        self.assertSilentVector(net.motorInput, net.NYAREAS * net.N1)
        self.assertSilentVector(net.sensPatt, net.NYAREAS*net.P*net.N1)
        self.assertSilentVector(net.motorPatt, net.NYAREAS*net.P*net.N1)
        self.assertSilentVector(net.J, net.NAREAS * net.NAREAS * net.NSQR1)
        self.assertSilentVector(net.Jinh, net.N1)
        self.assertSilentVector(net.linkffb, net.N1)
        self.assertSilentVector(net.linkrec, net.N1)
        self.assertSilentVector(net.linkinh, net.N1)
        self.assertSilentVector(net.tempffb, net.N1)
        self.assertSilentVector(net.clampSMIn, net.N1)
        self.assertSilentVector(net.freq_distrib, net.P)
        self.assertEqual(net.noise_fac, 6.928203230275509)

    def test_resetNet(self):
        net = StandardNet6Areas()
        net.main_init()

        # make sure there is non-zero activity in the network
        net.MAIN_INIT_RANDOM_ACTIVITY()

        self.assertVectorWithActivity(net.pot)
        self.assertVectorWithActivity(net.inh)
        self.assertVectorWithActivity(net.adapt)
        self.assertVectorWithActivity(net.rates)
        self.assertVectorWithActivity(net.slowinh)
        self.assertVectorWithActivity(net.tot_LTP)
        self.assertVectorWithActivity(net.tot_LTD)
        self.assertVectorWithActivity(net.above_hstory)
        self.assertTrue(net.total_output > 0)

        # then check that the reset zeroes all activity
        net.resetNet()

        self.assertSilentVector(net.pot, net.NAREAS * net.N1)
        self.assertSilentVector(net.inh, net.NAREAS * net.N1)
        self.assertSilentVector(net.adapt, net.NAREAS * net.N1)
        self.assertSilentVector(net.rates, net.NAREAS * net.N1)
        self.assertSilentVector(net.slowinh, net.NAREAS)
        self.assertSilentVector(net.tot_LTP, net.NAREAS)
        self.assertSilentVector(net.tot_LTD, net.NAREAS)
        self.assertSilentVector(
            net.above_hstory, net.NAREAS * net.N1 * net.P)
        self.assertEqual(net.total_output, 0.0)

    def test_init(self):
        net = StandardNet6Areas()
        net.main_init()

        # generate vectors with random activity
        net.INIT_RANDOM_ACTIVITY()

        # check that init recreates the vectors with the same shape but zero activity
        net.init()

        self.assertSilentVector(net.pot, net.NAREAS * net.N1)
        self.assertSilentVector(net.rates, net.NAREAS * net.N1)
        self.assertSilentVector(net.adapt, net.NAREAS * net.N1)
        self.assertSilentVector(net.avg_patts, net.NAREAS * net.N1 * net.P)
        self.assertSilentVector(net.ca_patts, net.NAREAS * net.N1 * net.P)
        self.assertSilentVector(net.ca_ovlps, net.NAREAS * net.P * net.P)
        self.assertSilentVector(net.ovlps, net.NAREAS * net.P)
        self.assertSilentVector(net.inh, net.NAREAS * net.N1)
        self.assertSilentVector(net.slowinh, net.NAREAS)
        self.assertSilentVector(net.sensInput, net.NYAREAS * net.N1)
        self.assertSilentVector(net.motorInput, net.NYAREAS * net.N1)
        self.assertSilentVector(net.above_thresh, net.NAREAS * net.N1)
        self.assertSilentVector(net.above_hstory, net.NAREAS * net.N1 * net.P)
        self.assertSilentVector(net.freq_distrib, net.P)

        self.assertEqual(net.total_output, 0.0)
        self.assertTrue(sum(1 for element in net.J if element != 0) > 0)
        self.assertVectorWithActivity(net.sensPatt)
        self.assertVectorWithActivity(net.motorPatt)

        # TODO test that this is initialised properly (need to mock random)
        # self.assertSilentVector(net.diluted, net.NAREAS * net.N1)

    def test_step(self):
        """
        Nothing to assert for now, just tests that it runs without failing
        """
        net = StandardNet6Areas()
        net.main_init()
        net.init()

        for i in range(100):
            net.step()

    @patch('random.random')
    def test_SFUNC(self, mock_random):
        net = StandardNet6Areas()

        mock_random.return_value = 0.5
        self.assertTrue(net.SFUNC(1.0))

        mock_random.return_value = 0.8
        self.assertFalse(net.SFUNC(0))


if __name__ == "__main__":
    unittest.main()
