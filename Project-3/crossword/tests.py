from generate import *
import unittest


class GenerateTestClass(unittest.TestCase):
    def setUp(self):
        structure = "data/structure1.txt"
        words = "data/words1.txt"
        # Generate crossword
        self.crossword = Crossword(structure, words)
        self.creator = CrosswordCreator(self.crossword)

    def test_enforce_node_constistency(self):
        self.creator.enforce_node_consistency()

        self.assertEqual(
            {Variable(2, 1, 'down', 5):
             {'FALSE', 'GRAPH', 'BAYES', 'START', 'DEPTH',
                 'ALPHA', 'INFER', 'PRUNE', 'LOGIC', 'TRUTH'},
             Variable(1, 12, 'down', 7): {'RESOLVE', 'MINIMAX', 'NETWORK', 'INITIAL', 'BREADTH'},
             Variable(6, 5, 'across', 6): {'MARKOV', 'NEURAL', 'REASON', 'SEARCH', 'CREATE'},
             Variable(1, 7, 'down', 7): {'RESOLVE', 'MINIMAX', 'NETWORK', 'INITIAL', 'BREADTH'},
             Variable(4, 4, 'across', 5): {'FALSE', 'GRAPH', 'BAYES', 'START', 'DEPTH', 'ALPHA', 'INFER', 'PRUNE', 'LOGIC', 'TRUTH'},
             Variable(2, 1, 'across', 12): {'INTELLIGENCE', 'SATISFACTION', 'DISTRIBUTION', 'OPTIMIZATION'}
             },
            self.creator.domains,
            msg="Node consistency not enforced"
        )


if __name__ == '__main__':
    unittest.main()
