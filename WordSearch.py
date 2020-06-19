"""
Implements a Word Search board given a list of words as a 2D Array.

Alex Eidt
"""

import string
import random
import pandas as pd

class WordSearch:
    """
    The WordSearch class abstracts a Word Search board as a 2D array
    first filled with all the words given in different orientations,
    and then fills the rest of the empty spaces with random letters.
    """

    def __init__(self, size, words):
        """
        Initializes an instances of a WordSearch class.
        """
        self.size = size
        self.words = list(set(map(str.upper, words)))

        # Check to see if the longest word in the words list is
        # less than the size of the board + 2 to ensure that
        # all words can be successfully placed on the board.
        assert self.size - max(map(len, self.words)) > 2, \
            f'Board Size {self.size} is too small.'

        random.shuffle(self.words)
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.word_coords = {}

        # Fill the board with words
        check = False
        while not check:
            self.init_board()
            check = self.fill_with_words()

        self.fill_board()
        
    def get_stats(self, word_len):
        """
        Gets the orientation and starting point of a word. "Stats"
        refers to the starting (x, y) coordinate and the steps (ox, oy)
        for a given word.

        Parameters
            word_len: The length of the word that the "stats" are being
                      found for

        Returns
            A tuple containing the starting coordinates and the step size
            in the x and y direction.
        """
        starty = startx = 0
        endy = endx = self.size

        orient = random.choice(range(0, 4))

        if orient == 0: # Horizontal
            ox = 1
            oy = 0
            endx = self.size - word_len # board columns - word_len
        elif orient == 1: # Vertical Down
            ox = 0
            oy = 1
            endy = self.size - word_len # board rows - word_len
        elif orient == 2: # Upward Diagonal
            ox = 1
            oy = -1
            starty = word_len
            endx = self.size - word_len # board columns - word_len
        elif orient == 3: # Downward Diagonal
            ox = 1
            oy = 1
            endy = self.size - word_len
            endx = self.size - word_len # board columns - word_len

        x = random.choice(range(startx, endx))
        y = random.choice(range(starty, endy))

        return ox, oy, x, y

    def check_board(self, word, x, y, ox, oy):
        """
        Given a certain word with starting coordinates (x, y) and step
        size in the x and y direction (ox, oy), determines if it is
        possible to place that word in those coordinates on the board.

        Parameters
            word: The word that could be placed at the given coordinates
            x: Starting x coordinate
            y: Starting y coordinate
            ox: Step size in x direction
            oy: Step size in y direction

        Returns
            True if the word can be placed at the proposed location, False
            otherwise.
        """
        for i, letter in enumerate(word):
            x_coord = x + i * ox
            y_coord = y + i * oy
            if self.board[y_coord][x_coord] != letter and \
                self.board[y_coord][x_coord]:
                return False
        return True

    def add_word(self, word):
        """
        Adds a word to the Word Search board.

        Parameters
            word: The word being placed on the Word Search Board.

        Returns
            False if the word could not be placed on the board (ran into
            infinite loop). True if the word can be placed on the board.
        """
        ox, oy, x, y = self.get_stats(len(word))
        # Check to see if the randomly picked location from getStats is
        # viable for the given word. If not, it will continue to check
        # until a spot has been found.

        # Count exists to prevent an infinite loop from occurring.
        # Especially with small board sizes, it's possible that due to
        # the random placement of the words, the algorithm runs out
        # of valid spots for the word. The way to solve this is to
        # arbitrarily choose a large number and check if the number
        # of iterations has exceeded it.
        count = 0
        while not self.check_board(word, x, y, ox, oy):
            ox, oy, x, y = self.get_stats(len(word))
            count += 1
            # Check for infinite loop
            if count > 20000:
                return False
        
        self.word_coords[word] = set()
        for i, letter in enumerate(word):
            x_coord = x + i * ox
            y_coord = y + i * oy
            self.board[y_coord][x_coord] = letter
            self.word_coords[word].add((letter, x_coord, y_coord))

        return True

    def fill_board(self):
        """
        Fills all empty locations of the board with random letters.
        """
        for i in range(self.size):
            for j in range(self.size):
                if not self.board[i][j]:
                    self.board[i][j] = random.choice(string.ascii_uppercase)

    def init_board(self):
        """
        Initializes every location of the board to be None.
        """
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = None

    def fill_with_words(self):
        """
        Fills the board with the given list of words.

        Returns
            False if one of the words could not be added to the board.
            True if all words have been successfully added to the board.
        """
        for word in self.words:
            check = self.add_word(word)
            if not check:
                return False
        return True

    def __repr__(self):
        return f'''{pd.DataFrame(self.board).to_string()}
            \nSize: {self.size}x{self.size}
            \nWords: {self.words}
            \nNumber of Words: {len(self.words)}    
        '''

    def __str__(self):
        return pd.DataFrame(self.board).to_string(index=False, header=False)