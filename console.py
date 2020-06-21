"""
This script allows the user to start an instance of the WordBoard GUI
from the command line. The user may also customize their wordboard size,
color, and which words are put into the word board.

Alex Eidt
"""

from WordBoard import WordBoard

def main():
    """
    Prints an introduction to the program in the console and takes user
    input to change the defaults (if necessary).
    Starts a Word Search Game with the given defaults.
    """
    print('Welcome to the WordSearch creator!')
    print('This program creates Word Search Puzzles.')
    print()
    print('The menu has four buttons which perform the following functions:')
    print('\t1. New Words: Generate a new random set of words to search for.')
    print('\tA text file containing words separated by newline characters called words.txt must be present in the current directory in order for this feature to work.')
    print('\t2. Export: Creates a .html file containing the current Word Search grid as a HTML table, LaTeX Matrix and a String')
    print('\t3. Solution: Show the location of each word on the Word Search board. Toggles on/off')
    print('\t4. Reshuffle: Creates a new Word Search grid with the same words in new positions')
    print()
    print('Click the buttons on the grid corresponding to the found word to "find" words')
    print()
    print('Defaults ->', 'Size: 16x16,', 'Color: Yellow')
    print("If you'd like to change the defaults, enter the desired values in the prompts below:")
    size = input('Size (Return/Enter for Default): ')
    print('Check valid color options here: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter')
    print('Entering an invalid color option will break the program.')
    color = input('Color (Return/Enter for Default): ')
    print("If you'd like to add a custom word list to replace words.txt, place the file in this directory and enter the file name below. Make sure words are separated by newline characters: ")
    file_name = input('New Words File Name (Return/Enter for Default): ')
    print("If you'd like to create a customized Word Search, enter the words below, one at a time:")

    check = 'a'
    words = []
    while check:
        check = input('Next Word (Return/Enter to Quit/Stop): ')
        words.append(check)
    
    size = int(size) if size else 16
    color = color if color else 'yellow'
    file_name = file_name if file_name else 'words.txt'
    words = words[:-1] if words[:-1] else None
    
    WordBoard(size=size, color=color, file_name=file_name, words=words)


if __name__ == '__main__':
    main()