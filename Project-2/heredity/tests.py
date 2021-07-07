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
        self.genes_and_traits = dict_of_gene_and_trait(
            set(self.people.keys()), {"Harry"}, {"James"}, {"James"})

    def test_dict_of_gene_and_trait(self):
        self.assertEqual(
            {'Harry': (1, 0), 'James': (2, 1), 'Lily': (0, 0)}, self.genes_and_traits)
        # print(result)

    def test_prob_has_gene_no_parents(self):
        # For 0 genes
        prob = prob_has_gene(self.people, "Lily", self.genes_and_traits)
        self.assertEqual(prob, 0.96)

        # For 2 genes
        prob = prob_has_gene(self.people, "James", self.genes_and_traits)
        self.assertEqual(prob, 0.01)

    def test_prob_has_gene(self):
        # Test harry for genes
        prob = prob_has_gene(self.people, "Harry", self.genes_and_traits)
        self.assertEqual(prob, 0.9802)

    def test_joint_probability(self):
        joint_prob = joint_probability(
            self.people, {"Harry"}, {"James"}, {"James"})
        self.assertTrue(math.isclose(joint_prob, 0.0026643247488))


class UpdateAndNormaliseTestClass(unittest.TestCase):
    def setUp(self):
        self.people = {
            'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
            'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
            'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
        }
        self.genes_and_traits = dict_of_gene_and_trait(
            set(self.people.keys()), {"Harry"}, {"James"}, {"James"})
        self.probabilities = {
            'Harry': {
                'gene': {2: 0, 1: 0, 0: 0},
                'trait': {True: 0, False: 0}},
            'James': {
                'gene': {2: 0, 1: 0, 0: 0},
                'trait': {True: 0, False: 0}},
            'Lily': {
                'gene': {2: 0, 1: 0, 0: 0},
                'trait': {True: 0, False: 0}}
        }

    def test_update_func(self):
        # get the joint probability
        joint_prob = joint_probability(
            self.people, {"Harry"}, {"James"}, {"James"})

        # Pass to update to update the probabilities dict
        update(self.probabilities, {"Harry"}, {
               "James"}, {"James"}, joint_prob)

        # check the dict has been updated
        self.assertEqual(
            self.probabilities,
            {
                'Harry': {'gene': {2: 0, 1: 0.0026643247488, 0: 0}, 'trait': {True: 0, False: 0.0026643247488}},
                'James': {'gene': {2: 0.0026643247488, 1: 0, 0: 0}, 'trait': {True: 0.0026643247488, False: 0}},
                'Lily': {'gene': {2: 0, 1: 0, 0: 0.0026643247488}, 'trait': {True: 0, False: 0.0026643247488}}}
        )

        update(self.probabilities, {"Harry"}, {
               "James"}, {"James"}, joint_prob)

        # If this fails but the one before didn't then your update is not adding p instead it is replacing p every time
        self.assertEqual(self.probabilities, {
            'Harry': {'gene': {2: 0, 1: 0.0053286494976, 0: 0}, 'trait': {True: 0, False: 0.0053286494976}},
            'James': {'gene': {2: 0.0053286494976, 1: 0, 0: 0}, 'trait': {True: 0.0053286494976, False: 0}},
            'Lily': {'gene': {2: 0, 1: 0, 0: 0.0053286494976}, 'trait': {True: 0, False: 0.0053286494976}}}
        )


class NormalizeTestClass(unittest.TestCase):
    def setUp(self):
        self.probabilities = {
            'Harry': {'gene': {2: 0, 1: 0.0026643247488, 0: 0}, 'trait': {True: 0, False: 0.0026643247488}},
            'James': {'gene': {2: 0.0026643247488, 1: 0, 0: 0}, 'trait': {True: 0.0026643247488, False: 0}},
            'Lily': {'gene': {2: 0, 1: 0, 0: 0.0026643247488}, 'trait': {True: 0, False: 0.0026643247488}}
        }

    def test_normalize_func(self):
        # normalize the given probabilities.
        normalize(self.probabilities)
        self.assertEqual(
            self.probabilities,
            {'Harry': {'gene': {2: 0.0, 1: 1.0, 0: 0.0}, 'trait': {True: 0.0, False: 1.0}},
             'James': {'gene': {2: 1.0, 1: 0.0, 0: 0.0}, 'trait': {True: 1.0, False: 0.0}},
             'Lily': {'gene': {2: 0.0, 1: 0.0, 0: 1.0}, 'trait': {True: 0.0, False: 1.0}}}

        )


if __name__ == '__main__':
    unittest.main()
