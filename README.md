# CS50-Intro-to-AI
## Project 0
### Degrees
#### Specification
Complete the implementation of the shortest_path function such that it returns the shortest path from the person with id source to the person with the id target.
*   Assuming there is a path from the `source` to the `target`, your function should return a list, where each list item is the next `(movie_id, person_id)` pair in the path from the source to the target. Each pair should be a tuple of two `int`s.
    *   For example, if the return value of `shortest_path` were `[(1, 2), (3, 4)]`, that would mean that the source starred in movie 1 with person 2, person 2 starred in movie 3 with person 4, and person 4 is the target.
*   If there are multiple paths of minimum length from the source to the target, your function can return any of them.
*   If there is no possible path between two actors, your function should return `None`.
*   You may call the `neighbors_for_person` function, which accepts a person’s id as input, and returns a set of `(movie_id, person_id)` pairs for all people who starred in a movie with a given person.
#### Time scale: 2-5 hours
#### Comments: 
For testing, a good pair to use is tom Hanks to Dustin Hoffman, the output should be:
3 degrees of separation.
1: Tom Hanks and Kevin Bacon starred in Apollo 13
2: Kevin Bacon and Tom Cruise starred in A Few Good Men
3: Tom Cruise and Dustin Hoffman starred in Rain Man
Which is represented by this list of tuples:
Path:  [('95953', '163'), ('104257', '129'), ('112384', '102')]


