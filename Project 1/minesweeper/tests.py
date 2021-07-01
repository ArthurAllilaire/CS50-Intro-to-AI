from minesweeper import *
import unittest

board = Minesweeper()
board.print()


class TestAddKnowledge(unittest.TestCase):
    def setUp(self):
        self.AI = MinesweeperAI()

    def test_adding_safes(self):
      # Doesn't affect the other tests
        AI = self.AI
        AI.add_knowledge((4, 4), 0)
        print(AI.knowledge)
        print("Known safes:", AI.safes)
        print("Mines: ", AI.mines)
        print("Moves made:", AI.moves_made)

        self.assertEqual(AI.knowledge, [])
        self.assertEqual(AI.safes,
                         set([(4, 4), (5, 5), (3, 4), (4, 3), (5, 4), (4, 5), (3, 3), (5, 3), (3, 5)]))
        self.assertEqual(AI.mines, set())
        self.assertEqual(AI.moves_made, set([(4, 4)]))

    def test_adding_mines(self):
        AI = self.AI
        AI.add_knowledge((0, 0), 3)
        print(AI.knowledge)
        print("Known safes:", AI.safes)
        print("Mines: ", AI.mines)
        print("Moves made:", AI.moves_made)

        self.assertEqual(AI.knowledge, [])
        self.assertEqual(AI.safes,
                         set([(0, 0)]))
        self.assertEqual(AI.mines, set([(0, 1), (1, 0), (1, 1)]))
        self.assertEqual(AI.moves_made, set([(0, 0)]))

    def test_adding_knowledge(self):
      # Going to globally change the state of the AI, but will revert at the end of this function for other tests
        oldAI = self.AI
        self.add_knowledge((0, 0), 1)
        self.AI = oldAI

    def add_knowledge(self, cell, count):
        """ Globally changes the AI in self.AI by adding the sentence that is created through the cell and count that is passed in. The Knowledge passed in should be incomplete (no known mines or safes) """
        self.AI.add_knowledge(cell, count)

        sentence = Sentence(self.AI.nearby_cells(cell), count)

        self.assertEqual(self.AI.knowledge, [sentence])
        self.assertEqual(self.AI.safes,
                         set([cell]))
        self.assertEqual(self.AI.mines, set())
        self.assertEqual(self.AI.moves_made, set([cell]))

    def test_inferences(self):
        self.AI.add_knowledge((0, 0), 2)

        sentence1 = Sentence(self.AI.nearby_cells((0, 0)), 2)

        self.AI.add_knowledge((0, 2), 2)

        sentence2 = Sentence(self.AI.nearby_cells((0, 2)), 2)

        self.AI.add_knowledge((0, 3), 0)

        sentence3 = Sentence(self.AI.nearby_cells((0, 3)), 0)

        for sentence in self.AI.knowledge:
            print("sentence", sentence)
        print("Known safes:", self.AI.safes)
        print("Mines: ", self.AI.mines)
        print("Moves made:", self.AI.moves_made)


if __name__ == '__main__':
    unittest.main()
