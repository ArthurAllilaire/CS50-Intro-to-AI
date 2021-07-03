import unittest
from heredity import *
import math


class JointProbabilityTestClass(unittest.TestCase):
    def setUp(self):
        self.people = {
            'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
            'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
            'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
        }

    def test_dict_of_gene_and_trait(self):
        result = dict_of_gene_and_trait(
            set(self.people.keys()), {"Harry"}, {"James"}, {"James"})

        self.assertEqual(
            {'Harry': (1, 0), 'James': (2, 1), 'Lily': (0, 0)}, result)
        print(result)

    def test_prob_has_gene_no_parents(self):
        # For 0 genes
        prob = prob_has_gene(self.people, "Lily", 0)
        self.assertEqual(prob, 0.96)

        # For 2 genes
        prob = prob_has_gene(self.people, "James", 2)
        self.assertEqual(prob, 0.01)

    @unittest.skip("Not yet implemented")
    def test_prob_has_gene(self):
        # Test harry for genes
        prob = prob_has_gene(self.people, "Lily", 0)
        self.assertEqual(prob, 0.96)

    @unittest.skip("Not yet implemented")
    def test_joint_probability(self):
        joint_prob = joint_probability(
            self.people, {"Harry"}, {"James"}, {"James"})
        self.assertTrue(math.isclose(joint_prob, 0.0026643247488))


if __name__ == '__main__':
    unittest.main()
