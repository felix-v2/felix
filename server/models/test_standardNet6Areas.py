import unittest
from standardNet6Areas import StandardNet6Areas


class TestStandardNet6Areas(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
