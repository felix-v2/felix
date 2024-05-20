import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np


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
