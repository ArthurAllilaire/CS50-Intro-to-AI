import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells.copy()
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells.copy()
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        try:
            self.cells.remove(cell)
        # If the cell is not in the list then fact is useless
        except KeyError:
            pass
        else:
            # Mine removed decrease counter
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        try:
            self.cells.remove(cell)
        # If the cell is not in the list then fact is useless
        except KeyError:
            pass


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def nearby_cells(self, cell):
        """ Returns all the cells in a set that are adjacent to the cell passed in """
        exploreBottom = False
        exploreLeft = False
        exploreRight = False
        exploreTop = False
        # Should you explore the top? True if height of board - 1 is more than current height
        if cell[1] < self.height - 1:
            exploreTop = True

        # Should you explore the bottom? True if current height is more than or equal to 1
        if cell[1] >= 1:
            exploreBottom = True

        # Should you explore the right? True if width of board - 1 is more than current width
        if cell[0] < self.width - 1:
            exploreRight = True

        # Should you explore the lef? True if current width is more than or equal to 1
        if cell[0] >= 1:
            exploreLeft = True

        result = set()

        if exploreTop:
            # Add cell directly above
            result.add((cell[0], cell[1]+1))

            if exploreRight:
                # Add cell diagonally up and to the right
                result.add((cell[0]+1, cell[1]+1))

            if exploreLeft:
                # Add cell diagonally up and to the left
                result.add((cell[0]-1, cell[1]+1))

        if exploreBottom:
            # Add cell directly below
            result.add((cell[0], cell[1]-1))

            if exploreRight:
                # Add cell diagonally below and to the right
                result.add((cell[0]+1, cell[1]-1))

            if exploreLeft:
                # Add cell diagonally below and to the left
                result.add((cell[0]-1, cell[1]-1))

        if exploreRight:
            # Add cell to the right
            result.add((cell[0]+1, cell[1]))

        if exploreLeft:
            # Add cell to the left
            result.add((cell[0]-1, cell[1]))

        return result

    def check_knowledge(self):
        """ Checks that no additional cells can be categorised based on the AI's knowledge base - no inference used only if count is equal to cells """
        to_delete = []
        for i in range(len(self.knowledge)):
            sentence = self.knowledge[i]
            """ # Get rid of empty sets from knowledge
            if not sentence.cells:
                del sentence """
            mines = sentence.known_mines()
            safes = sentence.known_safes()
            # If sentence has any known mines
            if mines:
                # Then mark each one as a mine
                for mine in mines:
                    self.mark_mine(mine)

            # If sentence has any known safes
            if safes:
                # Then mark each one as a safe
                for safe in safes:
                    self.mark_safe(safe)

            if sentence.cells == set() or safes or mines:
                to_delete.append(i)

        # Delete all cells that are empty, done once finished looping over self.knowledge
        new_knowledge = []
        for i in range(len(self.knowledge)):
            # If the cell is not to_delete
            if i not in to_delete:
                new_knowledge.append(self.knowledge[i])

        self.knowledge = new_knowledge

    def check_inferences(self):
        """ add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge, using subsets """
        old_knowledge = self.knowledge.copy()
        print(len(old_knowledge))
        for sentence in old_knowledge:
            print(sentence)

            for other_sentence in old_knowledge:
                # Check if the other_sentence is a subset of sentence
                if sentence != other_sentence and sentence.cells.issuperset(other_sentence.cells):
                    # Create new set with cells not in subset
                    new_cells = sentence.cells.difference(
                        other_sentence.cells)
                    # Create new sentence with difference in counts
                    count_dif = sentence.count - other_sentence.count
                    # Add it to knowledge
                    self.knowledge.append(
                        Sentence(new_cells, count_dif)
                    )
        print(len(self.knowledge))

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)
        # 3) add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        near_cells = self.nearby_cells(cell)
        sentence_cells = set()
        for cell in near_cells:
            # If the state of the cell if unkown add to sentence
            if cell not in self.mines and cell not in self.safes:
                sentence_cells.add(cell)

        # Create new sentence based on cells and count and add to knowledge
        # Sentence after each turn is being duplicated 3 times
        newSentence = Sentence(sentence_cells, count)
        if newSentence not in self.knowledge:
            self.knowledge.append(newSentence)

        # 4) mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        self.check_knowledge()

        # 5) add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        self.check_inferences()
        # Check knowledge again
        self.check_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Get all safe moves that have not already been made
        safe_moves = self.safes.difference(self.moves_made)
        # IF the set is not empty
        if safe_moves:
            # Return the first safe move
            return safe_moves.pop()

        return None  # otherwise

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Construct a set with all possible random moves
        moves = set()
        for y in range(self.height):
            for x in range(self.width):
                cell = (x, y)
                moves.add(cell)

        # Remove moves that have already been chosen and are known to be mines
        moves = list(moves.difference(self.moves_made, self.mines))
        # If there are possible moves
        if moves:
            # Return a random cell from remainder
            return random.choice(moves)

        return None
