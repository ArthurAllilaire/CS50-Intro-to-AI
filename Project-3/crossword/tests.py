from generate import *
import unittest


class GenerateTestClass(unittest.TestCase):
    def setUp(self):
        structure = "data/structure1.txt"
        words = "data/words1.txt"
        # Generate crossword
        self.crossword = Crossword(structure, words)
        self.creator = CrosswordCreator(self.crossword)
        self.creator.enforce_node_consistency()

    def test_enforce_node_constistency(self):

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

    def test_revise(self):
        """Test to see if arc consistency is enforced"""

        for var in self.crossword.variables:
            for other_var in self.crossword.variables:
                if var != other_var:
                    return_val = self.creator.revise(var, other_var)
                    overlap = self.crossword.overlaps[var, other_var]
                    if overlap:
                        var_domain = self.creator.domains[var]
                        other_var_domain = self.creator.domains[other_var]
                        # Slice string to get the right overlap
                        sliced_var_domain = set()
                        other_sliced_var_domain = set()
                        for word in var_domain:
                            sliced_var_domain.add(word[overlap[0]])
                        for other_word in other_var_domain:
                            other_sliced_var_domain.add(
                                other_word[overlap[1]])

                        # Check to make sure that for every letter in sliced_var_domain there is a letter in the opposite domain that is compatible (i.e. is the same)
                        for letter in sliced_var_domain:
                            self.assertTrue(
                                letter in other_sliced_var_domain, f"The domains are not arc consistent, {var_domain} {other_var_domain}")

                    else:
                        # If there are no overlaps no changes to the variables should have been made
                        self.assertFalse(return_val)


if __name__ == '__main__':
    unittest.main()
