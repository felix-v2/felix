import unittest
from ..standardNet6Areas import StandardNet6Areas
import numpy as np
from ..util import Get_Vector


class TestInitKernels(unittest.TestCase):
    def test_init_gaussian_kernel(self):
        """
        This func is called by init_patchy_gaussian_kernel - see this function called repeatedly in the init() func.
        For each of the 36 area-area connections, we pass to the kern funcs a slice of J corresponding to its
        position in the linear sequence, e.g. for (0,0) pass J[0:390625].
        """
        net = StandardNet6Areas()
        net.main_init()

        mock_j = Get_Vector(net.NAREAS * net.NAREAS * net.NSQR1)
        j_section = mock_j[0:net.NSQR1]  # e.g area (0,0) recurrent connection
        self.assertTrue(np.all(j_section == 0))

        # this will create 25*25 kernels of size 19*19 (361)
        net.init_gaussian_kernel(net.N11, net.N12, net.NREC1, net.NREC2, j_section,
                                 net.SIGMAX_REC, net.SIGMAY_REC, net.J_REC_PROB)

        # check the first 361-element kernel was copied 624 times
        # so we have 625 identical kernels - one for each cell in the area - each with 361 elements
        kernel_1 = j_section[0:361]
        kernel_2 = j_section[361:722]
        self.assertTrue(not np.all(kernel_1 == 0))
        self.assertTrue(np.allclose(kernel_1, kernel_2))

        # just make sure only this area's section of J has been affected
        self.assertTrue(np.all(mock_j[net.NSQR1:] == 0))

    def test_init_inhibitory_gaussian_kernel(self):
        """
        See this function called in the init() func.
        "There is only 1 inhibitory kernel (FIXED & identical for all)"
        """
        net = StandardNet6Areas()
        net.main_init()

        # check initialised as empty (all zeroes)
        self.assertTrue(np.all(net.Jinh == 0))
        self.assertEqual(len(net.Jinh), 625)

        # this will create 1 (inhibitory) kernel of size 5*5
        net.init_gaussian_kernel(1, 1, net.NINH1, net.NINH2, net.Jinh,
                                 net.SIGMAX_INH, net.SIGMAY_INH, net.J_INH_INIT)

        self.assertEqual(sum(1 for weight in net.Jinh if weight != 0), 25)

        expected_gauss = [0.039923908554801, 0.084518915073756, 0.108524435145575, 0.084518915073756,
                          0.039923908554801, 0.084518915073756, 0.178926544615227, 0.229746231006064,
                          0.178926544615227, 0.084518915073756, 0.108524435145575, 0.229746231006064,
                          0.295,             0.229746231006064, 0.108524435145575, 0.084518915073756,
                          0.178926544615227, 0.229746231006064, 0.178926544615227, 0.084518915073756,
                          0.039923908554801, 0.084518915073756, 0.108524435145575, 0.084518915073756,
                          0.039923908554801]

        # first kernel (0,0) is created
        self.assertTrue(np.allclose(net.Jinh[0:25], expected_gauss))

        # the kernel is not copied to other locations, because there is only one inhibitory kernel
        # see net.init_gaussian_kernel(1, 1, ...) -> (nx*ny = 1*1)
        self.assertTrue(np.all(net.Jinh[25:] == 0))

    def test_init_patchy_gaussian_kernel(self):
        """
        See this function called repeatedly in the init() func.
        For each of the 36 area-area connections, we pass to the kern funcs a slice of J corresponding to its
        position in the linear sequence, e.g. for (0,0) pass J[0:390625].
        """
        net = StandardNet6Areas()
        net.main_init()

        mock_j = Get_Vector(net.NAREAS * net.NAREAS * net.NSQR1)
        j_section = mock_j[0:net.NSQR1]
        self.assertTrue(np.all(j_section == 0))

        net.init_patchy_gauss_kern(net.N11, net.N12, net.NREC1, net.NREC2, j_section,
                                   net.SIGMAX_REC, net.SIGMAY_REC, net.J_REC_PROB, net.J_UPPER)

        # there isn't much to check here unless we mock random to make it deterministic
        self.assertTrue(not np.all(j_section == 0))


if __name__ == "__main__":
    unittest.main()
