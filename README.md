# Word Search

This program creates Word Searches for you.

## Blank Word Search

<img src="Documentation/WordSearchBlank.PNG" style="width: 50%">

## Word Search Partially Filled Out

<img src="Documentation/WordSearchEarth.PNG" style="width: 50%">

## Word Search with Solution Shown

<img src="Documentation/WordSearchSolution.PNG" style="width: 50%">

## Word Search with Words Reshuffled

<img src="Documentation/WordSearchSolutionReshuffled.PNG" style="width: 50%">

## Word Search with New Random Words
<img src="Documentation/WordSearchNewWords.PNG" style="width: 50%">

## New Random Words Solution Shown

<img src="Documentation/WordSearchNewWordsSolution.PNG" style="width: 50%">


## Usage

`cd` into the directory containing these scripts and run
<br>

```
python console.py
```

<br>

The following is an example of the console output:

<br>
<br>

```
Welcome to the WordSearch creator!
This program creates Word Search Puzzles for you.

The menu has four buttons which perform the following functions:
        1. New Words: Generate a new random set of words to search for
        2. Export: Creates a .html file containing the current Word Search grid as a HTML table, LaTeX Matrix and a String
        3. Solution: Show the location of each word on the Word Search board. Toggles on/off
        4. Reshuffle: Creates a new Word Search grid with the same words in new positions

Click the buttons on the grid corresponding to the found word to "find" words

Defaults -> Size: 16x16, Color: Yellow
If you'd like to change the defaults, enter the desired values in the prompts below:
Size (Return/Enter for Default):
Check valid color options here: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
Color (Return/Enter for Default):
If you'd like to create a customized Word Search, enter the words below, one at a time:
Next Word (Return/Enter to Quit/Stop): Mercury
Next Word (Return/Enter to Quit/Stop): Venus
Next Word (Return/Enter to Quit/Stop): Earth
Next Word (Return/Enter to Quit/Stop): Mars
Next Word (Return/Enter to Quit/Stop): Jupiter
Next Word (Return/Enter to Quit/Stop): Saturn
Next Word (Return/Enter to Quit/Stop): Uranus
Next Word (Return/Enter to Quit/Stop): Neptune
Next Word (Return/Enter to Quit/Stop):
```

## Exporting

The Word Search boards can be exported as a `.html` file containing an `html` table of the Word Search grid, a LaTeX matrix version of the Word Search grid, and the word search grid as a String. The LaTeX grid for the example shown above is shown below:
<br>

$\begin{matrix}A & M & A & R & S & Q & U & U & U & J & M & O & Z & H & H & D \\ X & C & P & Q & M & U & O & E & L & C & N & E & Z & C & T & Q \\ X & U & N & A & C & K & U & D & E & R & K & A & F & F & M & A \\ Q & X & Y & A & Q & P & T & O & U & R & S & U & M & L & Q & Q \\ B & G & R & V & O & C & S & T & E & Y & W & J & Z & P & M & K \\ B & T & T & E & H & E & A & T & R & F & M & P & U & U & E & Q \\ X & J & G & N & W & S & I & U & Q & B & S & V & B & K & M & V \\ L & U & U & U & Q & P & C & G & W & P & L & B & O & R & P & A \\ D & Y & X & S & U & R & S & P & I & U & R & A & N & U & S & W \\ G & U & W & J & E & I & K & Z & N & H & Q & E & Z & F & G & R \\ K & H & J & M & F & D & L & D & T & M & T & C & H & F & C & F \\ N & E & P & T & U & N & E & R & O & V & Y & T & F & L & S & Z \\ K & P & P & Q & W & Q & A & X & X & T & V & J & D & M & W & V \\ K & M & C & Q & E & E & L & Q & S & C & W & B & C & M & L & M \\ I & W & B & Z & V & S & H & B & O & O & Y & D & W & U & R & N \\ U & H & B & F & X & R & Q & S & H & O & Q & M & D & S & D & H\end{matrix}$