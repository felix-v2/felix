import unittest
import numpy as np
from .. import correlation


class TestCorrelate2dCyclicPython(unittest.TestCase):
    def test_small_vectors(self):
        width = 3
        height = 3
        kernel_width = 2
        kernel_height = 2

        in_vector = np.array(
            [0.2, 0.1, 0.4, 0.04, 0.8, 0.61, 0.37, 0.22, 0.74])
        kern = np.array([0.8, 0.1, 0.22, 0.51])
        out_vector = np.zeros(width * height)

        result = correlation.Correlate_2d_cyclic_python(
            in_vector, kern, width, height, kernel_width, kernel_height, out_vector)

        expected_output = np.array(
            [0.5868, 0.6071, 0.4946, 0.3056, 1.1268, 0.8435, 0.413, 0.476, 0.819])
        np.testing.assert_allclose(result, expected_output)

    def test_large_vectors(self):
        """
        Uses the kinds of data structures and variables passed to the func during the real step() during
        simulations
        """
        width = 25
        height = 25
        kernel_width = 19
        kernel_height = 19

        in_vector = np.random.rand(625)
        kern = np.random.rand(625)
        out_vector = np.zeros(625)

        result = correlation.Correlate_2d_cyclic_python(
            in_vector, kern, width, height, kernel_width, kernel_height, out_vector)

        self.assertEqual(len(result), 625)
        self.assertTrue(np.all(result != 0))


class TestCorrelate2dUniCyclic(unittest.TestCase):
    def test_small_vectors(self):
        input_matrix = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        uniform_kernel = np.array(
            [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2])
        out = np.zeros_like(input_matrix)

        got = correlation.Correlate_2d_Uni_cyclic(
            input_matrix, uniform_kernel, 3, 3, 3, 3, out)
        expected = np.array([54, 54, 54, 54, 54, 53, 54, 54, 54])

        np.testing.assert_array_equal(got, expected)

    def test_large_vectors(self):
        """
        Uses the kinds of data structures and variables passed to the func during the real step() during
        simulations
        """
        in_vector = np.random.rand(625)
        uniform_kern = np.full(625, 0.2)
        out_vector = np.zeros(625)

        result = correlation.Correlate_2d_Uni_cyclic(
            in_vector, uniform_kern, 25, 25, 19, 19, out_vector)

        self.assertEqual(len(result), 625)
        self.assertTrue(np.all(result != 0))


if __name__ == "__main__":
    unittest.main()
