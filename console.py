from WordBoard import WordBoard

def main():
    """
    Prints an introduction to the program in the console and takes user
    input to change the defaults (if necessary).
    Starts a Word Search Game with the given defaults.
    """
    print('Welcome to the WordSearch creator!')
    print('This program creates Word Search Puzzles for you.')
    print()
    print('The menu has four buttons which perform the following functions:')
    print('\t1. New Words: Generate a new random set of words to search for')
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
    color = input('Color (Return/Enter for Default): ')
    print("If you'd like to create a customized Word Search, enter the words below, one at a time:")

    check = 'a'
    words = []
    while check:
        check = input('Next Word (Return/Enter to Quit/Stop): ')
        words.append(check)
    
    size = int(size) if size else 16
    color = color if color else 'yellow'
    words = words[:-1] if words[:-1] else None
    
    WordBoard(size=size, color=color, words=words)


if __name__ == '__main__':
    main()