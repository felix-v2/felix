import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np
from unittest.mock import patch
from util import Get_Vector


class TestInitKernels(unittest.TestCase):

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

    @patch('random.random')
    def test_init_patchy_gaussian_kernel(self, mock_random):
        mock_random.return_value = 0.5

        net = StandardNet6Areas()
        net.main_init()

        mock_j = Get_Vector(net.NAREAS * net.NAREAS * net.NSQR1)
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


if __name__ == "__main__":
    unittest.main()
