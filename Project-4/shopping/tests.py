import unittest
from shopping import *


class LoadDataTestClass(unittest.TestCase):
    def setUp(self):
        self.data = load_data("shopping.csv")
        self.evidence = self.data[0]
        self.labels = self.data[1]

    def test_length(self):
        self.assertEqual(len(self.evidence), len(
            self.labels), msg=f"Length of evidence ({len(self.evidence)}) and labels ({len(self.labels)}) not the same.")

    def test_evidence(self):
        exemplar = [0, 0.0, 0, 0.0, 1, 0.0, 0.2,
                    0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0]
        self.assertEqual(
            self.evidence[0],
            exemplar,
            msg=f'The evidence should be: {exemplar}, but evidence for 1st customer is: {self.evidence[0]}')

    def test_labels(self):
        self.assertEqual(
            self.labels[0], 0, msg=f'The value should be 0, it is {self.labels[0]}')


if __name__ == '__main__':
    unittest.main()
