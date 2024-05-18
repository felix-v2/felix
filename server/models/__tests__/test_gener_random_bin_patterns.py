import unittest
from standardNet6Areas import StandardNet6Areas
import numpy as np
from unittest.mock import patch


class TestGenerRandomBinPatterns(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
