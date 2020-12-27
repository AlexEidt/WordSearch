"""
Implements a Word Search board given a list of words as a 2D Array.
This class can be implemented on its own without WordBoard.py.

After instantiation, the 2D Array containing all the letters of the board
as well as the solutions can be accessed as follows:

word_search = WordSearch()
2d_board = word_search.board
solutions = word_search.solutions

Alex Eidt
"""

from random import choice, shuffle

class WordSearch:
    """
    The WordSearch class abstracts a Word Search board as a 2D array
    first filled with all the words given in different orientations,
    and then fills the rest of the empty spaces with random letters.
    """

    def __init__(self, size, words):
        """
        Initializes an instances of a WordSearch class.

        Parameters
            size: Size of the board. Board will always be a square of size x size letters
            words: List of words to be hidden in the word search
        """
        self._size = size
        self._words = list(set(map(str.upper, words)))

        # Check to see if the longest word in the words list is
        # less than the size of the board + 2 to ensure that
        # all words can be successfully placed on the board.
        assert self._size - max(map(len, self._words)) > 2, \
            f'Board Size {self._size} is too small.'

        shuffle(self._words)
        self.board = [[None for _ in range(self._size)] for _ in range(self._size)]

        # Solutions is a mapping of words hidden in the board to a set of coordinates
        # of each letter in these words
        self.solutions = {}

        # Fill the board with words
        check = False
        while not check:
            self._init_board()
            check = self._fill_with_words()

        self._fill_board()
        
    def _get_orientation(self, word_len):
        """
        Gets the orientation and starting point of a word.
        Refers to the starting (x, y) coordinate and the steps (ox, oy)
        for a given word.

        Parameters
            word_len: The length of the word that the "stats" are being
                      found for

        Returns
            A tuple containing the starting coordinates and the step size
            in the x and y direction.
        """
        starty = startx = 0
        endy = endx = self._size

        orient = choice(range(0, 4))

        if orient == 0: # Horizontal
            ox = 1
            oy = 0
            endx = self._size - word_len # board columns - word_len
        elif orient == 1: # Vertical Down
            ox = 0
            oy = 1
            endy = self._size - word_len # board rows - word_len
        elif orient == 2: # Upward Diagonal
            ox = 1
            oy = -1
            starty = word_len
            endx = self._size - word_len # board columns - word_len
        elif orient == 3: # Downward Diagonal
            ox = 1
            oy = 1
            endy = self._size - word_len
            endx = self._size - word_len # board columns - word_len

        x = choice(range(startx, endx))
        y = choice(range(starty, endy))

        return x, y, ox, oy

    def _check_board(self, word, x, y, ox, oy):
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

    def _add_word(self, word):
        """
        Adds a word to the Word Search board.

        Parameters
            word: The word being placed on the Word Search Board.

        Returns
            False if the word could not be placed on the board (ran into
            infinite loop). True if the word can be placed on the board.
        """
        x, y, ox, oy = self._get_orientation(len(word))
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
        while not self._check_board(word, x, y, ox, oy):
            x, y, ox, oy = self._get_orientation(len(word))
            count += 1
            # Check for infinite loop
            if count > 20000:
                return False
        
        self.solutions[word] = set()
        for i, letter in enumerate(word):
            x_coord = x + i * ox
            y_coord = y + i * oy
            self.board[y_coord][x_coord] = letter
            self.solutions[word].add((letter, x_coord, y_coord))

        return True

    def _fill_board(self):
        """
        Fills all empty locations of the board with random letters.
        """
        for i in range(self._size):
            for j in range(self._size):
                if not self.board[i][j]:
                    self.board[i][j] = choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def _init_board(self):
        """
        Initializes every location of the board to be None.
        """
        for i in range(self._size):
            for j in range(self._size):
                self.board[i][j] = None

    def _fill_with_words(self):
        """
        Fills the board with the given list of words.

        Returns
            False if one of the words could not be added to the board.
            True if all words have been successfully added to the board.
        """
        for word in self._words:
            check = self._add_word(word)
            if not check:
                return False

        return True

    def __len__(self):
        """
        Returns the length of one side of the board.
        """
        return self._size

    def __str__(self):
        """
        Returns Word Search Board as a String.
        """
        output = []
        for i in range(self._size):
            output.append(' '.join(self.board[i]))

        return '\n'.join(output)