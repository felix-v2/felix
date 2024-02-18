import unittest
import numpy as np
import util


class TestUtil(unittest.TestCase):
    def test_Get_Vector(self):
        expected = np.zeros(10)
        got = util.Get_Vector(10)

        np.testing.assert_array_equal(expected, got)

    def test_Clear_Vector(self):
        v = util.Get_Vector(10)
        util.Clear_Vector(10, v)

        np.testing.assert_array_equal(v, np.zeros(10))

    def test_Get_bVector(self):
        expected = np.zeros(10)
        got = util.Get_bVector(10)

        np.testing.assert_array_equal(expected, got)

    def test_Clear_bVector(self):
        v = util.Get_bVector(10)
        util.Clear_bVector(10, v)

        np.testing.assert_array_equal(v, np.zeros(10))

    def test_equal_noise(self):
        self.assertTrue(0 <= util.equal_noise() <= 1)

    def test_bool_noise(self):
        self.assertFalse(util.bool_noise(0))
        self.assertTrue(util.bool_noise(1))
        self.assertIn(util.bool_noise(0.5), [True, False])

    def test_bSum(self):
        v = [1, 0, 1, 1, 0, 0, 0, 1]
        self.assertEqual(util.bSum(len(v), v), 4)

    def test_Sum(self):
        v = [1.1, 6.9, 2.2, 4.8, 9.7, 3.3, 8.5, 5.5]
        self.assertEqual(util.Sum(len(v), v), 42)

    def test_bSkalar(self):
        v1 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        v2 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

        got = util.bSkalar(len(v1), v1, v2)
        expected = 30

        self.assertEqual(got, expected)

    def test_bbSkalar(self):
        v1 = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        v2 = [1, 1, 0, 0, 1, 1, 1, 1, 0, 1]

        got = util.bbSkalar(len(v1), v1, v2)
        expected = 3

        self.assertEqual(got, expected)

    def test_Max_Elem(self):
        v = [1.1, 6.9, 2.2, 4.8, 9.7, 3.3, 8.5, 5.5]
        self.assertEqual(util.Max_Elem(len(v), v), 9.7)

    def test_Fire(self):
        vektor = [1.1, 2, 2.2, 3.3, 0.0]
        n = len(vektor)
        teta = 2
        dest = [1, 0, 1, 0, 1]

        got = util.Fire(n, vektor, teta, dest)
        expected = [0, 0, 1, 1, 0]

        self.assertEqual(got, expected)

    def test_leaky_integrate(self):
        tau = 0.1
        obj = 0.0
        expr = 1.0
        step_size = 1

        got = util.leaky_integrate(tau, obj, expr, step_size)
        expected = 10

        self.assertEqual(got, expected)

    def test_Correlate_2d_cyclic(self):
        input_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        kernel = np.array([[0.1, 1.4, 0.1], [1.4, 1.4, 1.4], [0.1, 1.4, 0.1]])
        out = np.zeros_like(input_matrix)

        got = util.Correlate_2d_cyclic(input_matrix, kernel, out)
        expected = np.array([[26, 29, 31], [34, 36, 39], [42, 44, 47]])

        np.testing.assert_array_equal(got, expected)

    def test_Correlate_2d_Uni_cyclic(self):
        input_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        uniform_kernel = np.array(
            [[1.2, 1.2, 1.2], [1.2, 1.2, 1.2], [1.2, 1.2, 1.2]])

        out = np.zeros_like(input_matrix)

        got = util.Correlate_2d_Uni_cyclic(input_matrix, uniform_kernel, out)
        expected = np.array([[54, 54, 54], [54, 54, 53], [54, 54, 54]])

        np.testing.assert_array_equal(got, expected)


if __name__ == "__main__":
    unittest.main()
