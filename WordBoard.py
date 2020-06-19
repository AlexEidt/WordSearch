
import os
import random
import tkinter as tk
import tkinter.font as tkFont
from functools import partial
from WordSearch import WordSearch


class WordBoard:

    def __init__(self, size=16, color='yellow', words=None):
        self.root = tk.Tk()
        self.root.title('Word Search')
        self.root.resizable(width=False, height=False)

        self.word_grid = tk.Frame(self.root)
        self.word_list = tk.Frame(self.root)
        self.menu = tk.Frame(self.root)

        self.solution_shown = False
        self.size = size
        self.color = color

        # Buttons that have been pushed
        self.pushed = set()
        
        self.words = words
        if self.words is None:
            self.choose_random_words()
        
        self.size = size
        self.buttons = [[None for _ in range(self.size)] 
                        for _ in range(self.size)]
        
        self.labels = {}
        self.word_search = WordSearch(self.size, self.words)
        self.create_labels()
        self.reshuffle()

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
        for label in self.labels.values():
            label.grid_remove()
        self.labels.clear()
        self.labels = {'Words': tk.Label(self.word_list, text='Words', pady=5, font=tkFont.Font(weight='bold'))}
        self.labels['Words'].grid(row=2, column=0, columnspan=2)
        for i, word in enumerate(sorted(self.word_search.words)):
            self.labels[word] = tk.Label(self.word_list, text=word, anchor='w')
            self.labels[word].grid(row=(i // 2) + (i % 1) + 3, column=i % 2, sticky='W')

    def choose_random_words(self):
        self.words = []
        with open('words.txt', mode='r') as f:
            wordstxt = f.read().split('\n')
            wordstxt = list(filter(lambda x: len(x) < self.size - 3, wordstxt))
            for _ in range(random.choice(range(self.size // 3, self.size))):
                self.words.append(random.choice(wordstxt))
            del wordstxt

    def pressed(self, row, col):
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
        if self.solution_shown:
            self.solution_shown = not self.solution_shown
        self.word_search = WordSearch(self.size, self.words)
        self.pushed.clear()

        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j] = tk.Button(
                    self.word_grid, text=self.word_search.board[i][j], 
                    padx=5, command=partial(self.pressed, i, j)
                )
                self.buttons[i][j].grid(row=i, column=j, sticky='ew')

        for label in self.labels.values():
            label.configure(bg='SystemButtonFace')

    def select_new(self):
        self.choose_random_words()
        self.reshuffle()
        self.create_labels()

    def export(self):
        number = 0
        file_name = 'WordSearch.html'
        while file_name in os.listdir(os.getcwd()):
            number += 1
            file_name = f'WordSearch{number}.html'
        
        del number

        with open(file_name, mode='w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('<head>\n')
            f.write('\t<title>Word Search</title>\n')
            f.write('''\t<script type="text/x-mathjax-config">
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
            for i in range(self.size):
                f.write(f"{''.join(self.word_search.board[i])} ::::: ")
            f.write('</div>\n')
            f.write('</html>')