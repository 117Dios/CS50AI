# ruff: noqa: F403, F405 (Warning suppression for wildstar imports)

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
    And(Or(AKnight,AKnave),Not(And(AKnight,AKnave))),
    
    Implication(AKnight,And(AKnave,AKnight)),
    Implication(AKnave,Not(And(AKnight,AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnight,AKnave),Not(And(AKnight,AKnave))),
    And(Or(BKnight,BKnave),Not(And(BKnight,BKnave))),
    
    Implication(AKnight,And(BKnave,AKnave)),
    Implication(AKnave,Not(And(BKnave,AKnave))),
    
    Or(BKnight,BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight,AKnave),Not(And(AKnight,AKnave))),
    And(Or(BKnight,BKnave),Not(And(BKnight,BKnave))),
    
    Implication(AKnight,Or(Biconditional(AKnight,BKnight), Biconditional(AKnave,BKnave))),
    Implication(AKnave,Not(Or(Biconditional(AKnight,BKnight), Biconditional(AKnave,BKnave)))),
    
    Implication(BKnight,Or(Biconditional(AKnight,BKnave), Biconditional(AKnave,BKnight))),
    Implication(BKnave,Not(Or(Biconditional(AKnight,BKnave), Biconditional(AKnave,BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnight,AKnave),Not(And(AKnight,AKnave))),
    And(Or(BKnight,BKnave),Not(And(BKnight,BKnave))),
    And(Or(CKnight,CKnave),Not(And(CKnight,CKnave))),
    
    Implication(Or(AKnight,AKnave),Or(AKnight,AKnave)),
    
    Implication(BKnight,Implication(AKnight,AKnave)),
    Implication(BKnave,Not(Implication(AKnight,AKnave))),
    Implication(BKnight,CKnave),
    Implication(BKnave,Not(CKnave)),
    
    Implication(CKnight,Implication(AKnight,AKnight)),
    Implication(CKnave,Not(Implication(AKnight,AKnight)))
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
