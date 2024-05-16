import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np
from unittest.mock import patch
from util import Get_Vector


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
        self.assertEqual(net.total_output, 0.0)

        self.assertSilentVector(net.freq_distrib, net.P)

        # @todo mock init_kern funcs and test them in isolation
        self.assertTrue(sum(1 for element in net.J if element != 0) > 0)

        # @todo test that this is initialised properly (need to mock random)
        # self.assertSilentVector(net.diluted, net.NAREAS * net.N1)

        # @todo mock gener_random_bin_activity
        # self.assertVectorWithActivity(net.sensPatt)
        # self.assertVectorWithActivity(net.motorPatt)

    @patch('random.random')
    def test_init_patchy_gaussian_kernel(self, mock_random):
        mock_random.return_value = 0.5

        net = StandardNet6Areas()
        net.main_init()

        mock_j = Get_Vector(net.NAREAS * net.NAREAS *
                            net.NSQR1)
        net.init_patchy_gauss_kern(net.N11, net.N12, net.NREC1, net.NREC2, mock_j[1:2],
                                   net.SIGMAX_REC, net.SIGMAY_REC, net.J_REC_PROB, net.J_UPPER)

    # @todo: this is weird because its a static method but we're passing into class variables
    def test_init_gaussian_kernel(self):
        net = StandardNet6Areas()
        net.main_init()

        StandardNet6Areas.init_gaussian_kernel(1, 1, net.NINH1, net.NINH2, net.Jinh,
                                               net.SIGMAX_INH, net.SIGMAY_INH, net.J_INH_INIT)

        self.assertEqual(len(net.Jinh), 625)
        self.assertEqual(sum(1 for element in net.Jinh if element != 0), 25)

        self.assertTrue(np.allclose(net.Jinh[0:25], [0.039923908554801, 0.084518915073756, 0.108524435145575, 0.084518915073756,
                                                     0.039923908554801, 0.084518915073756, 0.178926544615227, 0.229746231006064,
                                                     0.178926544615227, 0.084518915073756, 0.108524435145575, 0.229746231006064,
                                                     0.295,             0.229746231006064, 0.108524435145575, 0.084518915073756,
                                                     0.178926544615227, 0.229746231006064, 0.178926544615227, 0.084518915073756,
                                                     0.039923908554801, 0.084518915073756, 0.108524435145575, 0.084518915073756,
                                                     0.039923908554801]))

    @patch('random.choice')
    def test_gener_random_bin_patterns(self, mock_choice):
        net = StandardNet6Areas()
        net.main_init()

        cells = 625
        cellsToActivate = 19
        patterns = 12
        inputPat = np.zeros(patterns*cells, dtype=np.int32)

        # mock random: return a 1d array, all zeros except one active cell
        mock_choice.return_value = np.concatenate(
            (np.zeros(cellsToActivate-1), [1]))

        binPatterns = net.gener_random_bin_patterns(
            cells, cellsToActivate, patterns, inputPat)

        # we expect 12 patterns - each pattern is a set of 625 cells with a random number of cells activated
        self.assertEqual(binPatterns.shape, (12, 625))
        self.assertTrue(not np.all(binPatterns == 0))

    @patch('random.choice')
    def test_gener_random_bin_patterns_linear(self, mock_choice):
        net = StandardNet6Areas()
        net.main_init()

        cells = 625
        cellsToActivate = 19
        patterns = 12
        inputPat = np.zeros(patterns*cells, dtype=np.int32)

        # mock random: return a 1d array, all zeros except one active cell
        mock_choice.return_value = np.concatenate(
            (np.zeros(cellsToActivate-1), [1]))

        binPatterns = net.gener_random_bin_patterns_linear(
            cells, cellsToActivate, patterns, inputPat)

        # we expect 12 patterns - each pattern is a set of 625 cells with a random number of cells activated
        self.assertEqual(binPatterns.shape, (12*625, ))
        self.assertTrue(not np.all(binPatterns == 0))

    @patch('random.random')
    def test_SFUNC(self, mock_random):
        net = StandardNet6Areas()

        mock_random.return_value = 0.5
        self.assertTrue(net.SFUNC(1.0))

        mock_random.return_value = 0.8
        self.assertFalse(net.SFUNC(0))


class TestSetUpCurrentSensorimotorInput(unittest.TestCase):
    @staticmethod
    def assertSilentVector(arr: np.array, n: int):
        """
        Testing util func: asserts the 1d array with {els} elements, all with zero values.
        Aka an initialised empty vector (after main_init, but before simulation has started)
        """
        np.testing.assert_array_equal(arr, np.zeros(n))

    def test_copies_pattern_1(self):
        net = StandardNet6Areas()
        net.main_init()
        net.init()
        noise = .0001 * 200

        # check we start wth "empty" input areas and random patts
        self.assertSilentVector(net.sensInput, 625)
        self.assertSilentVector(net.motorInput, 625)
        self.assertTrue(not np.all(net.sensPatt == 0))
        self.assertTrue(not np.all(net.motorPatt == 0))

        net.sSInp = True
        net.sMInp = True
        net.sSInRow = 1
        net.sMInRow = 1
        net.spatno = 1
        net.strainNet = False
        net.training_phase = 100
        net.set_up_current_sensorimotor_input(noise)

        # check patt 1 is copied to input areas
        self.assertTrue(not np.all(net.sensInput == 0))
        self.assertTrue(not np.all(net.motorInput == 0))
        self.assertTrue(np.allclose(net.sensInput, net.sensPatt[0:625]))
        self.assertTrue(np.allclose(net.motorInput, net.motorPatt[0:625]))

    def test_copies_pattern_2(self):
        net = StandardNet6Areas()
        net.main_init()
        net.init()
        noise = .0001 * 200

        # check we start wth "empty" input areas and random patts
        self.assertSilentVector(net.sensInput, 625)
        self.assertSilentVector(net.motorInput, 625)
        self.assertTrue(not np.all(net.sensPatt == 0))
        self.assertTrue(not np.all(net.motorPatt == 0))

        net.sSInp = True
        net.sMInp = True
        net.sSInRow = 1
        net.sMInRow = 1
        net.strainNet = False
        net.training_phase = 100
        net.spatno = 2
        net.set_up_current_sensorimotor_input(noise)

        # check patt 2 is copied to input areas
        self.assertTrue(not np.all(net.sensInput == 0))
        self.assertTrue(not np.all(net.motorInput == 0))
        self.assertTrue(np.allclose(
            net.sensInput, net.sensPatt[625:1250]))
        self.assertTrue(np.allclose(net.motorInput, net.motorPatt[625:1250]))

    def test_no_patterns_only_whitenoise(self):
        net = StandardNet6Areas()
        net.main_init()
        net.init()
        noise = .0001 * 200

        # check we start wth "empty" input areas and random patts
        self.assertSilentVector(net.sensInput, 625)
        self.assertSilentVector(net.motorInput, 625)
        self.assertTrue(not np.all(net.sensPatt == 0))
        self.assertTrue(not np.all(net.motorPatt == 0))

        net.sSInp = False  # "don't copy sensory pattern to sensory input area"
        net.sMInp = False  # "don't copy motor pattern to motor input area"
        net.sSInRow = 1
        net.sMInRow = 1
        net.spatno = 1
        net.strainNet = False
        net.training_phase = 100
        net.set_up_current_sensorimotor_input(noise)

        # only whitenoise is added - the patterns are not copied to input areas
        self.assertTrue(not np.all(net.sensInput == 0))
        self.assertTrue(not np.all(net.motorInput == 0))
        self.assertFalse(np.allclose(net.sensInput, net.sensPatt[0:625]))
        self.assertFalse(np.allclose(net.motorInput, net.motorPatt[0:625]))

    def test_no_patterns_no_whitenoise(self):
        net = StandardNet6Areas()
        net.main_init()
        net.init()
        noise = .0001 * 200

        # check we start wth "empty" input areas and random patts
        self.assertSilentVector(net.sensInput, 625)
        self.assertSilentVector(net.motorInput, 625)
        self.assertTrue(not np.all(net.sensPatt == 0))
        self.assertTrue(not np.all(net.motorPatt == 0))

        net.sSInp = False  # "don't copy sensory pattern to sensory input area"
        net.sMInp = False  # "don't copy motor pattern to motor input area"
        net.sSInRow = 1
        net.sMInRow = 1
        net.spatno = 1
        net.strainNet = True
        net.training_phase = 2
        net.set_up_current_sensorimotor_input(noise)

        # patterns not copied to input areas; no whitenoise generated in input areas
        self.assertSilentVector(net.sensInput, 625)
        self.assertSilentVector(net.motorInput, 625)


if __name__ == "__main__":
    unittest.main()
