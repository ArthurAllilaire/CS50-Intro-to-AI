import unittest
from questions import *


class LoadFilesTestClass(unittest.TestCase):
    def setUp(self):
        self.data = load_files("corpus")
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


if __name__ == '__main__':
    unittest.main()
