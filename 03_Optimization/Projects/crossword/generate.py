import sys

from crossword import *
from collections import deque

# ruff: noqa: F403, F405

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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        
        for v in self.domains:
            for x in set(self.domains[v]):
                if len(x) != v.length:
                    self.domains[v].remove(x)
   

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revised = False
                
        overlap = self.crossword.overlaps[x,y]
        
        if overlap is None:
            return revised
        
        i, j = overlap
        
        for word_x in set(self.domains[x]):
            overlaps = False
            for word_y in self.domains[y]:
                if word_x[i] == word_y[j]:
                    overlaps = True
                    break
            if not overlaps:
                self.domains[x].remove(word_x)
                revised = True
        
        return revised
                

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = deque()
        
        if arcs is None:
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                        queue.append((x,y))
        else:
            queue.extend(arcs)
                
        while len(queue) > 0:
            x, y = queue.popleft()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z,x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        for variable in assignment:
            word = assignment[variable]
            
            if len(word) != variable.length:
                return False
            
            for variable_2 in assignment:
                if variable != variable_2 and assignment[variable_2] == word:
                    return False
            
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[variable,neighbor]
                    if overlap is not None:
                        i, j = overlap
                        if word[i] != assignment[neighbor][j]:
                            return False
        
        return True
                                  

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        lcv_list = []
        
        for word in self.domains[var]:
            counter = 0
            
            for neighbor in self.crossword.neighbors(var): 
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var,neighbor]
                    if overlap is not None:
                        i, j = overlap
                        for value in self.domains[neighbor]:
                            if word[i] != value[j]:
                                counter += 1
                                           
            lcv_list.append((counter, word))
        
        lcv_list.sort(key= lambda count: count[0])
        
        return [node for _, node in lcv_list]
                        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        assignment_list = []
        
        for var in self.crossword.variables:
            if var not in assignment:
                domain_size = len(self.domains[var])
                neighbor_num = len(self.crossword.neighbors(var))
                assignment_list.append((domain_size,neighbor_num,var))
        
        assignment_list.sort(key= lambda numbers: (numbers[0],numbers[1]))
        
        return assignment_list[0][2]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                
                temp_assignment = assignment.copy()
                
                temp_assignment[var] = value
                
                if self.consistent(temp_assignment):
                    result = self.backtrack(temp_assignment)
                    if result is not None:
                        return result
                    
                # L'implementazione di remove [{var = value}] from [assignment] qui non serve perché ho creato una copia di assignment sopra
                # Quindi se il risultato non è buono, semplicemente non ritorno nulla e "brucio" la copia nel processo.

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

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
