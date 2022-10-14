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
        #print(cell)
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
        #print(f"cells = {self.cells}")
        #print(f"length of cells = {len(self.cells)}")
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        emptySet = set()
        if len(self.cells) == self.count:
            newSet = set(self.cells)
            return newSet
        else:
            return emptySet

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        '''
        emptySet = set()
        print(f"self.cells = {self.cells}")
        if self.count == 0 and len(self.cells) > 0 and emptySet not in self.cells and self.cells != {0}: #maybe? 1 or 0
            newSet = self.cells.copy()
            print(f"newset = {newSet}")
            return newSet
        else:
            return None
            '''
        if self.count == 0 and len(self.cells) > 0:
            return self.cells
        else:
            return set()            

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


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
        #print(cell)
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

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
        #1
        self.moves_made.add(cell)
        #2
        self.mark_safe(cell)
        #3
        newCells = set()
        #print(cell[0])
        #print(cell[1])
        for i in range(-1, 2): #-1, 0, 1
            for j in range(-1, 2):
                row = cell[0] + i
                column = cell[1] + j

                if row < 0 or row > self.height - 1:
                    row = cell[0]
                if column < 0 or column > self.width - 1:
                    column = cell[1]
                
                newCell = (row, column)

                if newCell not in newCells:
                #if newCell not in newCells:
                    newCells.add(newCell)

        self.knowledge.append(Sentence(newCells, count))
        '''
        if cell[0] - 1 >= 0 and cell[0] + 1 <= self.height:
            if cell[1] - 1 >= 0 and cell[0] + 1 <= self.width:
                newCell = (cell[0] + i, cell[1] + j)
        '''

                
        #4 len known mines, len known safes not == 0, markmine, marksafe
        
        # tutorial
        for sentence in self.knowledge:
            if sentence.known_mines() != set():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            if sentence.known_safes() != set():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)
        
        '''
        for sentence in self.knowledge:
            print(sentence.__str__())
            if sentence.known_mines() != None and len(sentence.known_mines()) != 0:
                for mine in sentence.known_mines():
                    self.mark_mine(mine)
            if sentence.known_safes() != None and len(sentence.known_safes()) != 0:
                for safe in sentence.known_safes():
                    print(f"safe = {sentence.known_safes()}")
                    if safe != None:
                        self.mark_safe(safe)
        '''
        


        #5 get sentence, check if other sentences contain it as a subset, do math, keep doing in loop
        
        changeFlag = 0
        newKnowledge = []

        while (changeFlag == 1):
            changeFlag == 0
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    # Not doing anything because object pointer???????
                    if sentence1 != sentence2:
                        #If sentence cells are in sentence2 cells, do math
                        if sentence1.cells < sentence2.cells:
                            sentence1Set = set(sentence1.cells)
                            sentence2Set = set(sentence2.cells)
                            
                            #set2 - set1
                            sentence2Set -= sentence1Set
                            count = sentence2.count - sentence1.count
                            newKnowledge.append(Sentence(sentence2Set, count))
                            
                            #start looping again
                            changeFlag = 1
                # break loop
            self.knowledge += newKnowledge
        
        for mine in self.mines:
            print(f"mines - {mine}")
        for safe in self.safes:
            print(f"safes - {safe}")
        '''
        for sentence in self.knowledge:
            print()
            for cell in sentence.cells:
                print(f"cells in sentence - {cell}")
            print(f"sentence count --- {sentence.count}")                
            for safes in sentence.known_safes():
                print(f"safe cell - {safes}")
        '''
            #ADD NEW INFORMATION OF SAFE AND MINES!?!?!?
            # Maybe move while loop back one?

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for move in self.safes:
            if move not in self.moves_made:
                #print(f"self.safes = {self.safes}")
                #print(f"self.moves_made = {self.moves_made}")
                #print(f"move = {move}")
                return move
        #no safe moves
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        move = set()

        possibleMoves = []

        for i in range(self.height):
            for j in range(self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    possibleMoves.append(move)

        move = random.choice(possibleMoves)
        if move != set():
            return move
        else:
            return None

