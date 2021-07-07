import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # For every varaibles domain
        for var in self.domains:
            # Go through every word in the domain
            set_for_itr = self.domains[var].copy()
            for word in set_for_itr:
                # If it is not equal to the length of the variable
                if len(word) != var.length:
                    # remove it
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        # If no overlaps return False
        if not overlap:
            return False

        # Slice y domain to get the overlapping letters
        y_sliced_domain = set()
        for word in self.domains[y]:
            y_sliced_domain.add(word[overlap[1]])

        x_domain = self.domains[x].copy()
        changed = False
        for word in x_domain:
            # If the word's letter doesn't have a constistent one in y's domain then delete it.
            if word[overlap[0]] not in y_sliced_domain:
                self.domains[x].remove(word)
                changed = True

        return changed

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.

        An arc is
        queue = all arcs in csp
        while queue non-empty:
        (X, Y) = Dequeue(queue)
        if Revise(csp, X, Y):
        if size of X.domain == 0:
        return false
        for each Z in X.neighbors - {Y}:
        Enqueue(queue, (Z,X))
        return true
        """
        if arcs == None:
            # Make queue equal to all the arcs available
            queue = []
            searched_var = []
            for var in self.crossword.variables:
                # Get the neighbours
                close = self.crossword.neighbors(var)
                for neighbor in close:
                    # If not already gone through neighbor's neighbor's then - avoid double counting and getting them both ways
                    if neighbor not in searched_var:
                        # Add them to the queue
                        queue.append((var, neighbor))
                # Add the var as explored
                searched_var.append(var)
        else:
            queue = list(arcs)

        while queue:
            # Get the first arc from the queue
            # Split it into the two connected variables
            x, y = queue.pop(0)

            # Make the arc consistent
            if self.revise(x, y):
                # Check to make sure there are still possible solutions
                # If the domain is empty
                if not self.domains[x]:
                    # The problem is unsolvable
                    return False

                # Since X's domain has changed need to check all neighbouring domains to ensure arc consistency, bar y
                for neighbor in self.crossword.neighbors(x) - {y}:
                    # Add the arc to be checked for consistency
                    queue.append((neighbor, x))

        # Once all the arcs are consistent return True
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in assignment:
            if not assignment[var]:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # If not all vars have values
        if not self.assignment_complete(assignment):
            return False
        for var in assignment:
            word = assignment[var]
            # If string not the right size return false
            if len(word) != var.length:
                return False

            # If string not unique return False
            other_words = list(assignment.values())
            other_words.remove(word)
            if word in other_words:
                return False

            # If string conflicts with neighboring variables
                # Go through every neighbour
            for neighbor in self.crossword.neighbors(var):
                # Check for overlap
                overlap = self.crossword.overlaps[var, neighbor]
                # If they do overlap
                if overlap:
                    # Check that the overlapping letters aren't different
                    if word[overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False

        # If passed all the tests return True
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    print(sys.argv)
    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
