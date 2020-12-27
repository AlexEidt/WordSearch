"""
The WordBoard class is the GUI for the Word Search board.

Alex Eidt
"""

import tkinter as tk
import tkinter.font as tkFont
from os import listdir, getcwd
from random import choice
from functools import partial
from WordSearch import WordSearch

class WordBoard:
    """
    The WordBoard is the GUI for the WordSearch app. The grid is displayed
    on the left side of the app as a grid of buttons that capture which words
    have been found. The right side of the GUI features a menu allowing the user
    to see the solutions, reshuffle the board, or create a new board with
    completely new words (randomly chosen from words.txt/file_name). The user can also
    export the current board as an html file containing the board in html <table>,
    LaTeX and String form. This file also contains the solution.
    """

    def __init__(self, size=16, color='yellow', file_name='words.txt', words=None):
        """
        Initializes a WordBoard GUI.

        Parameters
            size: Size of the word search board. Default is 16x16. Size must be greater
                  than 3 otherwise an AssertionError is raised.
            color: Background color to indicated pressed buttons and found word labels.
                   Default is yellow. Color must be a valid tkinter color or else
                   program will not work.
            file_name: File that contains a list of words separated by newline (\n)
                       characters. Used to select random words for the Word Search.
                       Default is words.txt. If no file is given or words.txt is not included
                       in the current directory and words is None, then a FileNotFoundError 
                       is raised.
            words: A list of words entered by the user. Allows for customized word searches
                   with custom words. Default is None. If words is None, then words will be
                   randomly chosen from words.txt or the file given by file_name.
        """
        assert size > 3, 'Size must be greater than 3'

        root = tk.Tk()
        root.title('Word Search')
        root.resizable(width=False, height=False)

        self._word_grid = tk.Frame(root)
        self._word_list = tk.Frame(root)
        self._menu = tk.Frame(root)

        self._solution_shown = False
        self._size = size
        self._color = color
        
        # If file_name is not present in the current directory, the
        # New Words button will be disabled.
        new_words_button = tk.DISABLED
        if file_name in listdir(getcwd()):
            new_words_button = tk.NORMAL
            with open(file_name, mode='r') as f:
                self._wordstxt = filter(None, f.read().split('\n'))
                self._wordstxt = list(filter(lambda x: len(x) < self._size - 3, self._wordstxt))
        elif words is None:
            raise FileNotFoundError(f'''{file_name} not present in the current directory. {file_name}
                                    must contain words separated by newline (\\n) characters.''')

        # Buttons that have been pushed
        self._pushed = set()
        
        self._words = words
        if self._words is None:
            self._choose_random_words()
        else:
            self._words = list(set(map(str.upper, self._words)))
        
        # Create empty SIZExSIZE grid of buttons
        self._buttons = []
        for i in range(self._size):
            row = []
            for j in range(self._size):
                row.append(tk.Button(
                    self._word_grid, padx=5, command=partial(self._pressed, i, j)
                ))
                row[-1].grid(row=i, column=j, sticky='ew')
            self._buttons.append(row)

        # Menu Buttons at the top right of the GUI
        # Menu Label
        tk.Label(
            self._menu, text='Menu', pady=5, font=tkFont.Font(weight='bold')
        ).grid(row=0, column=0, columnspan=2, sticky='ew')
        # "New Words" Button
        tk.Button(
            self._menu, text='New Words', padx=1, pady=1,
            state=new_words_button, command=self._select_new
        ).grid(row=1, column=0, sticky='ew')
        # "Export" Button
        self._export_button = tk.Button(self._menu, text='Export', padx=1, pady=1, command=self._export)
        self._export_button.grid(row=1, column=1, sticky='ew')
        # "Solution" Button
        tk.Button(
            self._menu, text='Solution', padx=1, pady=1, command=self._solution
        ).grid(row=2, column=0, sticky='ew')
        # "Reshuffle" Button
        tk.Button(
            self._menu, text='Reshuffle', padx=1, pady=1, command=self._reshuffle
        ).grid(row=2, column=1, sticky='ew')

        self._labels = {}
        self._word_search = None
        self._create_labels()
        self._reshuffle()

        self._word_grid.pack(side=tk.LEFT)
        self._menu.pack(side=tk.TOP, pady=self._size)
        self._word_list.pack(side=tk.TOP, padx=40, pady=20)

        tk.mainloop()

    def _create_labels(self):
        """
        Creates/changes the word labels on the right side of the GUI.
        """
        for label in self._labels.values():
            label.destroy()
        self._labels.clear()
        self._labels = {'Words': tk.Label(self._word_list, text='Words', pady=5, font=tkFont.Font(weight='bold'))}
        self._labels['Words'].grid(row=2, column=0, columnspan=2)
        for i, word in enumerate(sorted(self._words)):
            self._labels[word] = tk.Label(self._word_list, text=word, anchor='w')
            self._labels[word].grid(row=(i // 2) + (i % 1) + 3, column=i % 2, sticky='W')

    def _choose_random_words(self):
        """
        Chooses a random number of words (proportional to the size of the board)
        from the file_name file.
        """
        self._words = set()
        for _ in range(choice(range(self._size // 3, self._size))):
            self._words.add(choice(self._wordstxt).upper())
        self._words = list(self._words)

    def _pressed(self, row, col):
        """
        The command for every button in the board. Checks to see if a word
        has been found and disables all buttons associated with a word once
        found.

        Parameters
            row, col: The row and column index of the button in the self._buttons
                      list
        """
        if self._buttons[row][col].cget('bg') == self._color:
            self._buttons[row][col].configure(bg='SystemButtonFace')
            self._pushed.remove((self._buttons[row][col].cget('text'), col, row))
        else:
            self._buttons[row][col].configure(bg=self._color)
            self._pushed.add((self._buttons[row][col].cget('text'), col, row))
            for word, coords in self._word_search.solutions.items():
                if coords & self._pushed == coords:
                    for _, col, row in coords:
                        self._buttons[row][col].configure(state=tk.DISABLED)
                    self._labels[word].configure(bg=self._color)

    def _solution(self):
        """
        Command for the "Solution" button. Toggles the solutions on/off when
        pressed by lighting up the backgrounds of the buttons that contain
        the words in the board.
        """
        if self._solution_shown:
            bg = 'SystemButtonFace'
            state = tk.NORMAL
            self._pushed.clear()
        else:
            bg = self._color
            state = tk.DISABLED

        self._solution_shown = not self._solution_shown
        for word, coords in self._word_search.solutions.items():
            self._labels[word].configure(bg=bg)
            for _, col, row in coords:
                self._buttons[row][col].configure(state=state, bg=bg)

    def _reshuffle(self):
        """
        Command for the "Reshuffle" button. Uses the existing words and
        creates a new word search board with the words in new locations.
        """
        self._export_button.configure(text='Export', state=tk.NORMAL)

        if self._solution_shown:
            self._solution_shown = not self._solution_shown
        self._word_search = WordSearch(self._size, self._words)
        self._pushed.clear()

        for i in range(self._size):
            for j in range(self._size):
                self._buttons[i][j].configure(
                    text=self._word_search.board[i][j], bg='SystemButtonFace',
                    state=tk.NORMAL
                )

        for label in self._labels.values():
            label.configure(bg='SystemButtonFace')

    def _select_new(self):
        """
        Command for the "New Words" button. Chooses a new randoms set of
        words from the file_name file and fills up the board with the new
        words and displays it in the GUI.
        """
        self._choose_random_words()
        self._reshuffle()
        self._create_labels()

    def _export(self):
        """
        Command for the "Export" button. Creates an html file containing
        a html table and LaTeX version of the Word Search Board. Also
        contains the board as a string. Includes the solution and the words
        at the bottom of the page.
        """
        self._export_button.configure(state=tk.DISABLED)

        number = 0
        file_name = 'WordSearch.html'
        while file_name in listdir(getcwd()):
            number += 1
            file_name = f'WordSearch{number}.html'
        
        with open(file_name, mode='w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('<head>\n')
            f.write('\t<title>Word Search</title>\n')
            # Scripts required to display LaTeX
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
            for i in range(self._size):
                f.write('\t<tr>\n\t\t')
                for j in range(self._size):
                    f.write(f'<td padding=1em>{self._word_search.board[i][j]}</td>')
                f.write('\t</tr>\n')
            f.write('</table>\n<br><br>')

            # Create LaTeX Matrix of the Word Search Grid
            f.write('<h2 align="center">Latex WordSearch Grid:</h2>\n<br><br>')
            f.write('\\begin{matrix}')
            f.write(' \\\\ '.join([' & '.join(row) for row in self._word_search.board]))
            f.write('\\end{matrix}\n<br><br>')
            f.write('<h2 align="center">WordSearch Grid as String:</h2>\n<br><br>')

            # Create String Version of Word Search Grid. Each Row separated by ':::::'
            f.write('<div align="center">\n')
            f.write(' ::: '.join([''.join(self._word_search.board[i]) for i in range(self._size)]))
            f.write('\n<br><br>\n')
            f.write('\n'.join([''.join(self._word_search.board[i]) for i in range(self._size)]))
            f.write('</div>\n')

            # Add solution to the bottom of the file
            f.write('\n<br><br><h2 align="center">Solution</h2><br><br>\n')
            f.write('\\begin{matrix}')

            coordinates = set()
            for coords in self._word_search.solutions.values():
                for coord in coords:
                    coordinates.add(coord)

            board = []
            for i in range(self._size):
                row = []
                for j in range(self._size):
                    if (self._word_search.board[i][j], j, i) in coordinates:
                        row.append(self._word_search.board[i][j])
                    else:
                        row.append('')
                board.append(row)
            
            f.write(' \\\\ '.join([' & '.join(row) for row in board]))
            f.write('\\end{matrix}')

            # Add words used in the Word Search and the size of the board
            f.write('\n<br><br><h2 align="center">Words</h2><br><br>\n')
            f.write(f'''<ul align="center"><li>{'</li><li>'.join(self._words)}</li></ul>\n''')
            f.write(f'\n<br><br><h2 align="center">SIZE: {self._size}x{self._size}</h2><br><br>\n')
            f.write('</html>')

        self._export_button.configure(text='Exported')