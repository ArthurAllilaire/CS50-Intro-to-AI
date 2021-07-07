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
        # Go through all possible variable combinations
        for var in self.crossword.variables:
            for other_var in self.crossword.variables:
              # Don't test it on the same var
                if var != other_var:
                    begining_domain = self.creator.domains[var].copy()
                    return_val = self.creator.revise(var, other_var)
                    var_domain = self.creator.domains[var]
                    # If the begining domain is different to the end domain
                    if begining_domain != var_domain:
                        # return val should be true
                        self.assertTrue(
                            return_val, msg="Changes were made to domain but revise returned False"
                        )
                    # Else False
                    else:
                        self.assertFalse(
                            return_val, msg="No changes were made to domain but revise returned True"
                        )
                    overlap = self.crossword.overlaps[var, other_var]
                    if overlap:
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

    def test_ac3_with_arcs(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_ac3_without_arcs(self):
        """

        """
        self.creator.ac3()
        print(self.creator.domains)
        print(self.crossword.overlaps)
        result = {Variable(2, 1, 'down', 5): {'INFER'},
                  Variable(4, 4, 'across', 5): {'TRUTH', 'LOGIC', 'DEPTH'},
                  Variable(2, 1, 'across', 12): {'INTELLIGENCE'}, Variable(6, 5, 'across', 6): {'SEARCH', 'REASON', 'MARKOV'},
                  Variable(1, 12, 'down', 7): {'RESOLVE', 'NETWORK'},
                  Variable(1, 7, 'down', 7): {'MINIMAX', 'INITIAL', 'RESOLVE', 'NETWORK', 'BREADTH'}}
        # Order of the variables doesn't matter
        for var in self.creator.domains:
            self.assertEqual(
                self.creator.domains[var],
                result[var],
                msg=f"The domains are not right, actual domain: {self.creator.domains[var]}, correct domain: {result[var]}"
            )

    def test_assignment_complete(self):
        assignment = {}
        for var in self.crossword.variables:
            assignment[var] = "Word"

        self.assertTrue(self.creator.assignment_complete(
            assignment
        ))

        # Get rid of a word
        assignment[self.crossword.variables.pop()] = ""

        self.assertFalse(
            self.creator.assignment_complete(assignment)
        )

    def test_consistent(self):
        var_list = [Variable(1, 7, 'down', 7), Variable(1, 12, 'down', 7), Variable(4, 4, 'across', 5), Variable(
            2, 1, 'down', 5), Variable(6, 5, 'across', 6), Variable(2, 1, 'across', 12)]
        assignment = {}
        word_list = ["MINIMAX", "RESOLVE", "LOGIC",
                     "INFER", "SEARCH", "INTELLIGENCE"]

        for i in range(len(var_list)):
            assignment[var_list[i]] = word_list[i]

        self.assertTrue(
            self.creator.consistent(assignment), msg="Should return True as list of words is valid"
        )

        # Set a duplicate word
        assignment[var_list[0]] = word_list[1]

        # Should return False
        self.assertFalse(
            self.creator.consistent(assignment), msg="Should return False as list of words contains a duplicate"
        )

        # Set a word to empty
        assignment[var_list[0]] = ""

        # Should return False
        self.assertFalse(
            self.creator.consistent(assignment), msg="Should return False as list of words contains an empty string"
        )

        # Set a conflict on overlaps, A should be an I
        assignment[var_list[0]] = "MANIMAX"

        # Should return False
        self.assertFalse(
            self.creator.consistent(assignment), msg="Should return False as there is a conflict on the overlaps"
        )


if __name__ == '__main__':
    unittest.main()
