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
Spec: https://cs50.harvard.edu/ai/2020/projects/2/pagerank/#specification
#### Time scale: 1-2 days
#### Comments: 
I have written tests for all of the functions, stored in tests.py, you can copy the file and run them on you computer to check your implementation before submitting the code.

### Project 2b: Heredity
#### Specification:
Complete the implementations of joint_probability, update, and normalize.
Spec: https://cs50.harvard.edu/ai/2020/projects/2/heredity/#specification
#### Time scale: 1-3 days
#### Comments: 
Comprehensive tests in tests.py to help you debug, will show the cause of the problem.

## Project 3: Crossword
#### Specification:
Complete the implementation of enforce_node_consistency, revise, ac3, assignment_complete, consistent, order_domain_values, selected_unassigned_variable, and backtrack in generate.py so that your AI generates complete crossword puzzles if it is possible to do so.
Spec: https://cs50.harvard.edu/ai/2020/projects/3/crossword/#specification
#### Time scale: 1-3 days
#### Comments: 
Comprehensive tests in tests.py to help you debug, will show the cause of the problem.


## Project 4
### Project 4a: Shopping
#### Specification:
Complete the implementation of load_data, train_model, and evaluate in shopping.py.
Spec: https://cs50.harvard.edu/ai/2020/projects/4/shopping/#specification
#### Time scale: 2-3 hours
#### Comments: 
Not very extensive tests, but assignment is not very complicated.


### Project 4b: Nim
#### Specification:
Complete the implementation of get_q_value, update_q_value, best_future_reward, and choose_action in nim.py. For each of these functions, any time a function accepts a state as input, you may assume it is a list of integers. Any time a function accepts an action as input, you may assume it is an integer pair (i, j) of a pile i and a number of objects j.
Spec: https://cs50.harvard.edu/ai/2020/projects/4/nim/#specification
#### Time scale: 2-3 hours
#### Comments: 
No tests, but assignment is not very long.

## Project 5: Traffic
#### Specification:
Complete the implementation of load_data and get_model in traffic.py.
Spec: https://cs50.harvard.edu/ai/2020/projects/5/traffic/#specification
#### Time scale: 4 hours - 2 days
#### Comments: 
Check out the readme.md file that explains my process for hyperparameter optimization.

## Project 6a
### Project 6a: Parser
#### Specification:
Complete the implementation of preprocess and np_chunk, and complete the context-free grammar rules defined in NONTERMINALS.
Spec: https://cs50.harvard.edu/ai/2020/projects/6/parser/#specification
#### Time scale: 4 hours - 1 days


### Project 6b: Questions
#### Specification:
Complete the implementation of load_files, tokenize, compute_idfs, top_files, and top_sentences in questions.py.
Spec: https://cs50.harvard.edu/ai/2020/projects/6/questions/#specification
#### Time scale: 1 - 2 days
#### Comments: 
Small test suite that is not complete.
