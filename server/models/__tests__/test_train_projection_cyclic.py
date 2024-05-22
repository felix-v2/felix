import unittest
from standardNet6Areas import StandardNet6Areas
import json
import numpy as np


class TestTrainProjectionCyclic(unittest.TestCase):
    """
    This snippet from the original C code shows how the func is called, and with which args.

    In our Python implementation, for each vector, we pass in the numpy slice.
    For the LTD/LTP values to be incremented, instead of passing pointer args in,
    we just reference the class variables inside the func.

    /* Yes: train RECurrent kernel projections for this area   */
    train_projection_cyclic(
        &rates[N1 * j],               // pre-syn. rates
        &pot[N1 * i],                 // post-syn. pot.
        &J[NSQR1 * (NAREAS + 1) * j], // all (j+1)-->(j+1) kernels
        N11, N12, NREC1, NREC2, hrate, &tot_LTP[i], &tot_LTD[i]);
    """
    net = StandardNet6Areas()
    net.main_init()
    net.init()
    net.INIT_RANDOM_ACTIVITY()

    def test_between_area_projection(self):
        net = self.net

        dest_area_i = 1
        origin_area_j = 0

        # rates is a 1d numpy array with 6*625 elements (areas * cells per area)
        rates_start_idx = net.N1 * origin_area_j
        rates_end_idx = net.N1 * (origin_area_j + 1)
        rates = net.rates[rates_start_idx:rates_end_idx]

        # pot is a 1d numpy array with 6*625 elements (areas * cells per area)
        pot_start_idx = net.N1 * dest_area_i
        pot_end_idx = net.N1 * (dest_area_i + 1)
        pot = net.pot[pot_start_idx:pot_end_idx]

        # J is a 1d numpy array with 6*6*625*625 elements (areas * areas * cells per area * cells per area)
        k_start_idx = net.NSQR1 * (net.NAREAS * origin_area_j + dest_area_i)
        k_end_idx = k_start_idx + net.NSQR1
        kernels = net.J[k_start_idx:k_end_idx]

        # the func modifies it in place, so we create a copy here so we can compare with the post-execution value
        j_before = net.J.copy()
        pot_before = net.pot.copy()
        rates_before = net.rates.copy()

        print(json.dumps({
            'origin area': origin_area_j,
            'dest area': dest_area_i,
            'kernels for origin -> dest (start)': k_start_idx,
            'kernels for origin -> dest (end)': k_end_idx,
            'origin pre-synaptic firing rates (start)': rates_start_idx,
            'origin pre-synaptic firing rates (end)': rates_end_idx,
            'dest post-synaptic potentials (start)': pot_start_idx,
            'dest post-synaptic potentials (end)': pot_end_idx,
        }, sort_keys=False, indent=4))

        net.train_projection_cyclic(
            rates, pot, kernels, net.N11, net.N12, net.NREC1, net.NREC2, .0001 * 15, net.tot_LTP[dest_area_i:dest_area_i+1], net.tot_LTD[dest_area_i:dest_area_i+1])

        # check only the (area 0 -> area 1) section of J has changed
        self.assertTrue(np.allclose(
            j_before[0:k_start_idx], net.J[0:k_start_idx]))
        self.assertFalse(np.allclose(j_before, net.J))
        self.assertTrue(np.allclose(
            j_before[k_end_idx:], net.J[k_end_idx:]))

        # check rates and pot unaffected
        self.assertTrue(np.allclose(net.rates, rates_before))
        self.assertTrue(np.allclose(net.pot, pot_before))

        # check LTP and LTD updated only for the dest area
        self.assertTrue(all(val == 0 for i, val in enumerate(
            net.tot_LTP) if i != dest_area_i))
        self.assertTrue(net.tot_LTP[dest_area_i] > 0)
        self.assertTrue(all(val == 0 for i, val in enumerate(
            net.tot_LTD) if i != dest_area_i))
        self.assertTrue(net.tot_LTD[dest_area_i] > 0)


if __name__ == "__main__":
    unittest.main()
