import unittest
from ..standardNet6Areas import StandardNet6Areas
import numpy as np


class TestRecordAverageResponsesDuringTraining(unittest.TestCase):
    def test_pattern_is_averaged(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_rates = net.rates.copy()
        start_avg_patts = net.avg_patts.copy()

        # "averages for pattern 2 should be recorded"
        net.spatno = 2
        net.stps_2b_avgd = 100

        net.record_average_responses_during_training()

        # pot, adapt unchanged; rates, total_output updated
        self.assertTrue(np.allclose(net.rates, start_rates))
        self.assertFalse(np.allclose(net.avg_patts, start_avg_patts))
        self.assertEqual(net.stps_2b_avgd, 99)

    def test_pattern_is_not_averaged(self):
        net = StandardNet6Areas()
        net.main_init()

        # init with random vectors, and create copies to compare with values after
        net.INIT_RANDOM_ACTIVITY()
        start_rates = net.rates.copy()
        start_avg_patts = net.avg_patts.copy()

        # "no more steps remaining, do not average anymore"
        net.spatno = 2
        net.stps_2b_avgd = 0

        net.record_average_responses_during_training()

        # pot, adapt unchanged; rates, total_output updated
        self.assertTrue(np.allclose(net.rates, start_rates))
        self.assertTrue(np.allclose(net.avg_patts, start_avg_patts))
        self.assertEqual(net.stps_2b_avgd, 0)


if __name__ == "__main__":
    unittest.main()
