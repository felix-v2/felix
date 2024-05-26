import unittest
from ..standardNet6Areas import StandardNet6Areas
import numpy as np
from .. import util

# TODO


class TestComputeNewMembranePotentials(unittest.TestCase):
    def test_compute_new_membrane_potentials(self):
        net = StandardNet6Areas()
        net.main_init()
        net.init()

        # pot, inh, diluted
        # linkffb
        # tempffb
        # clampSMIn
        # sensInput, motorInput
        # J - unchaged
        # slowinh,linkinh,linkrec

        net.compute_new_membrane_potentials()


if __name__ == "__main__":
    unittest.main()
