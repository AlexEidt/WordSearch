
import string
import random
import pandas as pd

class WordSearch:

    def __init__(self, size, words):
        self.size = size
        self.words = list(set(map(str.upper, words)))

        assert self.size - max(map(len, self.words)) > 2, \
            f'Board Size {self.size} is too small.'

        random.shuffle(self.words)
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.word_coords = {}

        check = False
        while not check:
            self.init_board()
            check = self.fill_with_words()

        self.fill_board()
        
    def get_stats(self, word_len):
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
        for i, letter in enumerate(word):
            x_coord = x + i * ox
            y_coord = y + i * oy
            if self.board[y_coord][x_coord] != letter and \
                self.board[y_coord][x_coord]:
                return False
        return True

    def add_word(self, word):
        ox, oy, x, y = self.get_stats(len(word))
        # Check to see if the randomly picked location from getStats is
        # viable for the given word. If not, it will continue to check
        # until a spot has been found.

        # Count exists to prevent an infinite loop from occurring.
        # Especially with small board sizes, its possible that due to
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
        for i in range(self.size):
            for j in range(self.size):
                if not self.board[i][j]:
                    self.board[i][j] = random.choice(string.ascii_uppercase)

    def init_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = None

    def fill_with_words(self):
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