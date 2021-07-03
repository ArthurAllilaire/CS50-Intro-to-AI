# CS50-Intro-to-AI
## Project 0
### Projct 0a: Degrees
#### Specification
Complete the implementation of the shortest_path function such that it returns the shortest path from the person with id source to the person with the id target.
*   Assuming there is a path from the `source` to the `target`, your function should return a list, where each list item is the next `(movie_id, person_id)` pair in the path from the source to the target. Each pair should be a tuple of two `int`s.
    *   For example, if the return value of `shortest_path` were `[(1, 2), (3, 4)]`, that would mean that the source starred in movie 1 with person 2, person 2 starred in movie 3 with person 4, and person 4 is the target.
*   If there are multiple paths of minimum length from the source to the target, your function can return any of them.
*   If there is no possible path between two actors, your function should return `None`.
*   You may call the `neighbors_for_person` function, which accepts a person’s id as input, and returns a set of `(movie_id, person_id)` pairs for all people who starred in a movie with a given person.
#### Time scale: 2-5 hours
#### Comments: 
For testing, a good pair to use is tom Hanks to Dustin Hoffman in the small testing set, the output should be:
3 degrees of separation.
1. Tom Hanks and Kevin Bacon starred in Apollo 13
2. Kevin Bacon and Tom Cruise starred in A Few Good Men
3. Tom Cruise and Dustin Hoffman starred in Rain Man
* Which is represented by this list of tuples:
* Path:  [('95953', '163'), ('104257', '129'), ('112384', '102')]

### Projct 0b: Tic Tac Toe
#### Specification:
Complete the implementations of player, actions, result, winner, terminal, utility, and minimax.
For more detail: https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/
#### Time scale: 2-5 hours


## Project 1
### Project 1a: Knights
#### Specification:
Add knowledge to knowledge bases knowledge0, knowledge1, knowledge2, and knowledge3 to solve the following puzzles.
*   Puzzle 0 is the puzzle from the Background. It contains a single character, A.
    *   A says “I am both a knight and a knave.”
*   Puzzle 1 has two characters: A and B.
    *   A says “We are both knaves.”
    *   B says nothing.
*   Puzzle 2 has two characters: A and B.
    *   A says “We are the same kind.”
    *   B says “We are of different kinds.”
*   Puzzle 3 has three characters: A, B, and C.
    *   A says either “I am a knight.” or “I am a knave.”, but you don’t know which.
    *   B says “A said ‘I am a knave.’”
    *   B then says “C is a knave.”
    *   C says “A is a knight.”
In each of the above puzzles, each character is either a knight or a knave. Every sentence spoken by a knight is true, and every sentence spoken by a knave is false.

Once you’ve completed the knowledge base for a problem, you should be able to run python puzzle.py to see the solution to the puzzle.

#### Time scale: 1-2 hours

### Project 1b: Minesweeper
#### Specification:
Complete the implementations of the Sentence class and the MinesweeperAI class in minesweeper.py.
For more info: https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/
#### Time scale: 1-2 days
#### Comments: 
A lot harder than previous projects, but a very nice example of the power of inferences and knowledge combined with the speed and record keeping of a computer. I have added some rudimentary tests, but they are incomplete.

## Project 2
### Project 2a: Pagerank
#### Specification:
Complete the implementation of `transition_model`, `sample_pagerank`, and `iterate_pagerank`.

The `transition_model` should return a dictionary representing the probability distribution over which page a random surfer would visit next, given a corpus of pages, a current page, and a damping factor.

*   The function accepts three arguments: `corpus`, `page`, and `damping_factor`.
    *   The `corpus` is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    *   The `page` is a string representing which page the random surfer is currently on.
    *   The `damping_factor` is a floating point number representing the damping factor to be used when generating the probabilities.
*   The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing the probability that a random surfer would choose that page next. The values in this returned probability distribution should sum to `1`.
    *   With probability `damping_factor`, the random surfer should randomly choose one of the links from `page` with equal probability.
    *   With probability `1 - damping_factor`, the random surfer should randomly choose one of all pages in the corpus with equal probability.
*   For example, if the `corpus` were `{"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}`, the `page` was `"1.html"`, and the `damping_factor` was `0.85`, then the output of `transition_model` should be `{"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}`. This is because with probability `0.85`, we choose randomly to go from page 1 to either page 2 or page 3 (so each of page 2 or page 3 has probability `0.425` to start), but every page gets an additional `0.05` because with probability `0.15` we choose randomly among all three of the pages.
*   If `page` has no outgoing links, then `transition_model` should return a probability distribution that chooses randomly among all pages with equal probability. (In other words, if a page has no links, we can pretend it has links to all pages in the corpus, including itself.)

The `sample_pagerank` function should accept a corpus of web pages, a damping factor, and a number of samples, and return an estimated PageRank for each page.

*   The function accepts three arguments: `corpus`, a `damping_factor`, and `n`.
    *   The `corpus` is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    *   The `damping_factor` is a floating point number representing the damping factor to be used by the transition model.
    *   `n` is an integer representing the number of samples that should be generated to estimate PageRank values.
*   The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing that page’s estimated PageRank (i.e., the proportion of all the samples that corresponded to that page). The values in this dictionary should sum to `1`.
*   The first sample should be generated by choosing from a page at random.
*   For each of the remaining samples, the next sample should be generated from the previous sample based on the previous sample’s transition model.
    *   You will likely want to pass the previous sample into your `transition_model` function, along with the `corpus` and the `damping_factor`, to get the probabilities for the next sample.
    *   For example, if the transition probabilities are `{"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}`, then 5% of the time the next sample generated should be `"1.html"`, 47.5% of the time the next sample generated should be `"2.html"`, and 47.5% of the time the next sample generated should be `"3.html"`.
*   You may assume that `n` will be at least `1`.

The `iterate_pagerank` function should accept a corpus of web pages and a damping factor, calculate PageRanks based on the iteration formula described above, and return each page’s PageRank accurate to within `0.001`.

*   The function accepts two arguments: `corpus` and `damping_factor`.
    *   The `corpus` is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    *   The `damping_factor` is a floating point number representing the damping factor to be used in the PageRank formula.
*   The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing that page’s PageRank. The values in this dictionary should sum to `1`.
*   The function should begin by assigning each page a rank of `1 / N`, where `N` is the total number of pages in the corpus.
*   The function should then repeatedly calculate new rank values based on all of the current rank values, according to the PageRank formula in the “Background” section. (i.e., calculating a page’s PageRank based on the PageRanks of all pages that link to it).
    *   A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
*   This process should repeat until no PageRank value changes by more than `0.001` between the current rank values and the new rank values.
#### Time scale: 1-2 days
#### Comments: 
I have written tests for all of the functions, stored in tests.py, you can copy the file and run them on you computer to check your implementation before submitting the code.

### Project 2b:
#### Specification:
#### Time scale: 2-5 hours
#### Comments: 

## Project 1
### Project 1a:
#### Specification:
#### Time scale: 2-5 hours
#### Comments: 
### Project 1b:
#### Specification:
#### Time scale: 2-5 hours
#### Comments: 
