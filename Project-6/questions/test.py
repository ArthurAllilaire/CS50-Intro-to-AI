import unittest
from questions import *
import re


class TestClass(unittest.TestCase):
    def setUp(self):
        self.data = load_files("corpus")
        self.tokenize = tokenize(self.data["python.txt"])
        # print(self.data)

    def testLenData(self):
        self.assertEqual(len(self.data), 6)

    def testKeys(self):
        self.assertEqual(
            ['python.txt',
             'neural_network.txt',
             'machine_learning.txt',
             'artificial_intelligence.txt', 'natural_language_processing.txt',
             'probability.txt'],
            list(self.data.keys())
        )

    def testVal(self):
        self.assertTrue(
            isinstance(self.data["python.txt"], str)
        )

    def testTokenize(self):
        for word in self.tokenize:
            self.assertFalse(
                re.search("[^\w]", word)
            )


if __name__ == '__main__':
    unittest.main()
