from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a Knight or a Knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # IF A is a knight then A has to be both a knigt and a knave
    Implication(AKnight, And(AKnight, AKnave)),
    # ELSE if A is a knave then A cannot be both a knight and a knave
    Implication(AKnave, Not(And(AKnave, AKnight)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is either a Knight or a Knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is either a Knight or a Knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # IF A is a knight then B and A have to be knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # ELSE if A is a knave then A and B cannot both be knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is either a Knight or a Knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is either a Knight or a Knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # IF A is a knight then B and A have to be knaves or have to be knights
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, AKnave))),
    # ELSE if A is a knave then A and B cannot both be knaves
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, AKnave)))),

    # IF B is a knave then B and A have to be knaves or have to be knights
    Implication(BKnave, Or(And(AKnave, BKnave), And(AKnight, AKnave))),
    # ELSE if B is a knave then A and B cannot both be knaves or both be Knights
    Implication(BKnight, Not(Or(And(AKnave, BKnave), And(AKnight, AKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# Create symbols to use to represent whether A said something
IKnight = Symbol("A said I am a knight")
IKnave = Symbol("A said I am a knave")

knowledge3 = And(
    # A is either a Knight or a Knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is either a Knight or a Knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # C is either a Knight or a Knave but not both
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # A said either IKnight of Iknave but not both
    And(Or(IKnight, IKnave), Not(And(IKnight, IKnave))),

    # If A is a knight he must have said I am a knight
    Implication(AKnight, IKnight),
    # Elif A is a knave must have said I am a knight
    Implication(AKnave, IKnight),
    # Therefore A must have said IKnight

    # B says "A said 'I am a knave'."
    # If B is a knave then Not(IKnave)
    Implication(BKnave, Not(IKnave)),
    # If B is a knigth then A must have said I a knave
    Implication(BKnight, IKnave),

    # B says "C is a knave."
    # If B is a knave then C is not a knave
    Implication(BKnave, Not(CKnave)),
    # If B is a knigth then C must be a knave
    Implication(BKnight, CKnave),

    # C says "A is a knight."
    # If C is a knave then A is not a knight
    Implication(CKnave, Not(AKnight)),
    # If C is a knigth then A must be a knight
    Implication(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
