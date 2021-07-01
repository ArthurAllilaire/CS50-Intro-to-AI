import unittest
import math
from pagerank import *


class TransitionModelTestCase(unittest.TestCase):
    def setUp(self):
        self.corpus = {
            "1.html": {"2.html", "3.html"},
            "2.html": {"3.html"},
            "3.html": {"2.html"}
        }

    def test_no_link_page(self):
        corpus = self.corpus
        # Set 1.html to no links
        corpus["1.html"] = {}

        prob_dist = transition_model(corpus, "1.html", DAMPING)
        # Each probability should be 0.333 as only 3 pages
        for prob in prob_dist.values():
            self.assertTrue(math.isclose(prob, 1/3))

    def test_link_page(self):
        """ There may be a rounding error due to floats not being exact. """
        prob_dist = transition_model(self.corpus, "1.html", DAMPING)
        # Each probability should be 0.333 as only 3 pages
        self.assertEqual(
            prob_dist, {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475})


if __name__ == '__main__':
    unittest.main()
