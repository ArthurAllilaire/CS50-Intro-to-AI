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
        self.prob_dist = transition_model(self.corpus, "1.html", DAMPING)

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

        # Each probability should be 0.333 as only 3 pages
        self.assertEqual(
            self.prob_dist, {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475})

    def test_prob_dist_sum_to_one(self):
        self.assertTrue(sum(self.prob_dist.values()) == 1)


class SamplePagerankTestCase(unittest.TestCase):
    def setUp(self):
      # So all test outputs are the same use same random numbers
        random.seed(0)
        self.corpus = {
            "1.html": {"2.html", "3.html"},
            "2.html": {"3.html"},
            "3.html": {"2.html"}
        }
        self.pagerank = sample_pagerank(self.corpus, DAMPING, 100000)

    def test_pagerank_sums_to_one(self):
        self.assertTrue(sum(self.pagerank.values()) == 1)

    def test_pagerank(self):
        """ This is the test being done: but adding maths.isclose for rounding errors:
        self.assertEqual(
            self.pagerank, {'1.html': 0.05011, '2.html': 0.47548, '3.html': 0.47441}) """
        pages = ['1.html', '2.html', '3.html']
        keys = list(self.pagerank.keys())
        for i in range(len(keys)):
            page = keys[i]
            example_page = pages[i]
            self.assertEqual(page, example_page)

        example_values = [0.05011, 0.47548, 0.47441]
        values = list(self.pagerank.values())
        for i in range(len(values)):
            value = values[i]
            example_value = example_values[i]
            self.assertTrue(math.isclose(value, example_value))


class IteratePagerankTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()
