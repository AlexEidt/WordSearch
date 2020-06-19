"""
The WordBoard class is the GUI for the Word Search board.

Alex Eidt
"""

import os
import random
import tkinter as tk
import tkinter.font as tkFont
from functools import partial
from WordSearch import WordSearch

class WordBoard:
    """
    The WordBoard is the GUI for the WordSearch app. The grid is displayed
    on the left side of the app as a grid of buttons that capture which words
    have been found. The right side of the GUI features a menu allowing the user
    to see the solutions, reshuffle the board, or create a new board with
    completely new words (randomly chosen from words.txt). The user can also
    export the current board as an html file containing the board in html <table>,
    LaTeX and String form. This file also contains the solution.
    """

    def __init__(self, size=16, color='yellow', words=None):
        """
        Initializes a WordBoard GUI.
        """
        self.root = tk.Tk()
        self.root.title('Word Search')
        self.root.resizable(width=False, height=False)

        self.word_grid = tk.Frame(self.root)
        self.word_list = tk.Frame(self.root)
        self.menu = tk.Frame(self.root)

        self.solution_shown = False
        self.size = size
        self.color = color

        with open('words.txt', mode='r') as f:
            self.wordstxt = f.read().split('\n')
            self.wordstxt = list(filter(lambda x: len(x) < self.size - 3, self.wordstxt))

        # Buttons that have been pushed
        self.pushed = set()
        
        self.words = words
        if self.words is None:
            self.choose_random_words()
        else:
            self.words = list(set(words))
        
        self.size = size
        self.buttons = [[None for _ in range(self.size)] 
                        for _ in range(self.size)]
        
        self.labels = {}
        self.word_search = WordSearch(self.size, self.words)
        self.create_labels()
        self.reshuffle()

        # Menu Buttons at the top right of the GUI
        menu_label = tk.Label(self.menu, text='Menu', pady=5, font=tkFont.Font(weight='bold'))
        menu_label.grid(row=0, column=0, columnspan=2, sticky='ew')
        newwords_button = tk.Button(self.menu, text='New Words', padx=1, pady=1, command=self.select_new)
        newwords_button.grid(row=1, column=0, sticky='ew')
        words_button = tk.Button(self.menu, text='Export', padx=1, pady=1, command=self.export)
        words_button.grid(row=1, column=1, sticky='ew')
        solution_button = tk.Button(self.menu, text='Solution', padx=1, pady=1, command=self.solution)
        solution_button.grid(row=2, column=0, sticky='ew')
        reshuffle_button = tk.Button(self.menu, text='Reshuffle', padx=1, pady=1, command=self.reshuffle)
        reshuffle_button.grid(row=2, column=1, sticky='ew')

        self.word_grid.pack(side=tk.LEFT)
        self.menu.pack(side=tk.TOP, pady=20)
        self.word_list.pack(side=tk.TOP, padx=40, pady=20)

        tk.mainloop()

    def create_labels(self):
        """
        Creates/changes the word labels on the right side of the GUI.
        """
        for label in self.labels.values():
            label.destroy()
        self.labels.clear()
        self.labels = {'Words': tk.Label(self.word_list, text='Words', pady=5, font=tkFont.Font(weight='bold'))}
        self.labels['Words'].grid(row=2, column=0, columnspan=2)
        for i, word in enumerate(sorted(self.word_search.words)):
            self.labels[word] = tk.Label(self.word_list, text=word, anchor='w')
            self.labels[word].grid(row=(i // 2) + (i % 1) + 3, column=i % 2, sticky='W')

    def choose_random_words(self):
        """
        Chooses a random number of words (proportional to the size of the board)
        from the words.txt file.
        """
        self.words = []
        for _ in range(random.choice(range(self.size // 3, self.size))):
            self.words.append(random.choice(self.wordstxt))

    def pressed(self, row, col):
        """
        The command for every button in the board. Checks to see if a word
        has been found and disables all buttons associated with a word once
        found.
        """
        if self.buttons[row][col].cget('bg') == self.color:
            self.buttons[row][col].configure(bg='SystemButtonFace')
            self.pushed.remove((self.buttons[row][col].cget('text'), col, row))
        else:
            self.buttons[row][col].configure(bg=self.color)
            self.pushed.add((self.buttons[row][col].cget('text'), col, row))
            for word, coords in self.word_search.word_coords.items():
                if coords & self.pushed == coords:
                    for _, col, row in coords:
                        self.buttons[row][col].configure(state=tk.DISABLED)
                    self.labels[word].configure(bg=self.color)

    def solution(self):
        """
        Command for the "Solution" button. Toggles the solutions on/off when
        pressed by lighting up the backgrounds of the buttons that contain
        the words in the board.
        """
        if self.solution_shown:
            bg = 'SystemButtonFace'
            state = tk.NORMAL
        else:
            bg = self.color
            state = tk.DISABLED

        self.solution_shown = not self.solution_shown
        for word, coords in self.word_search.word_coords.items():
            self.labels[word].configure(bg=bg)
            for _, col, row in coords:
                self.buttons[row][col].configure(state=state, bg=bg)

    def reshuffle(self):
        """
        Command for the "Reshuffle" button. Uses the existing words and
        creates a new word search board with the words in new locations.
        """
        if self.solution_shown:
            self.solution_shown = not self.solution_shown
        self.word_search = WordSearch(self.size, self.words)
        self.pushed.clear()

        for i in range(self.size):
            for j in range(self.size):
                if self.buttons[i][j]:
                    self.buttons[i][j].destroy()
                self.buttons[i][j] = tk.Button(
                    self.word_grid, text=self.word_search.board[i][j], 
                    padx=5, command=partial(self.pressed, i, j)
                )
                self.buttons[i][j].grid(row=i, column=j, sticky='ew')

        for label in self.labels.values():
            label.configure(bg='SystemButtonFace')

    def select_new(self):
        """
        Command for the "New Words" button. Chooses a new randoms set of
        words from the words.txt file and fills up the board with the new
        words and displays it in the GUI.
        """
        self.choose_random_words()
        self.reshuffle()
        self.create_labels()

    def export(self):
        """
        Command for the "Export" button. Creates an html file containing
        a html table and LaTeX version of the Word Search Board. Also
        contains the board as a string. Includes the solution and the words
        at the bottom of the page.
        """
        number = 0
        file_name = 'WordSearch.html'
        while file_name in os.listdir(os.getcwd()):
            number += 1
            file_name = f'WordSearch{number}.html'
        
        with open(file_name, mode='w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('<head>\n')
            f.write('\t<title>Word Search</title>\n')
            f.write(
                '''\t<script type="text/x-mathjax-config">
                    MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\\\(','\\\\)']]}});
                    </script>
                    <script type="text/javascript"
                    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
                    </script>\n'''
            )
            f.write('</head>\n')
            f.write('<h2 align="center">HTML Table WordSearch Grid:</h2>\n<br><br>')

            # Create HTML Table Version of the Word Search Grid
            f.write('<table align="center">\n')
            for i in range(self.size):
                f.write('\t<tr>\n\t\t')
                for j in range(self.size):
                    f.write(f'<td padding=1em>{self.word_search.board[i][j]}</td>')
                f.write('\t</tr>\n')
            f.write('</table>\n<br><br>')

            # Create LaTeX Matrix of the Word Search Grid
            f.write('<h2 align="center">Latex WordSearch Grid:</h2>\n<br><br>')
            f.write('\\begin{matrix}')
            f.write(' \\\\ '.join([' & '.join(row) for row in self.word_search.board]))
            f.write('\\end{matrix}\n<br><br>')
            f.write('<h2 align="center">WordSearch Grid as String:</h2>\n<br><br>')

            # Create String Version of Word Search Grid. Each Row separated by ':::::'
            f.write('<div align="center">\n')
            f.write(' ::: '.join([''.join(self.word_search.board[i]) for i in range(self.size)]))
            f.write('\n<br><br>\n')
            f.write('\n'.join([''.join(self.word_search.board[i]) for i in range(self.size)]))
            f.write('</div>\n')

            # Add solution to the bottom of the file
            f.write('\n<br><br><h2 align="center">Solution</h2><br><br>\n')
            f.write('\\begin{matrix}')

            coordinates = set()
            for coords in self.word_search.word_coords.values():
                for coord in coords:
                    coordinates.add(coord)

            board = []
            for i in range(self.size):
                row = []
                for j in range(self.size):
                    if (self.word_search.board[i][j], j, i) in coordinates:
                        row.append(self.word_search.board[i][j])
                    else:
                        row.append('')
                board.append(row)
            
            f.write(' \\\\ '.join([' & '.join(row) for row in board]))
            f.write('\\end{matrix}')

            # Add words used in the Word Search and the size of the board
            f.write('\n<br><br><h2 align="center">Words</h2><br><br>\n')
            f.write(f'''<ul align="center"><li>{'</li><li>'.join(self.words)}</li></ul>\n''')
            f.write(f'\n<br><br><h2 align="center">SIZE: {self.size}x{self.size}</h2><br><br>\n')
            f.write('</html>')