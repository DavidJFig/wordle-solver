# wordle-solver
 
A script that solves the official Wordle automatically.

**Features**

Works on the actual Wordle website

Filters possible words based on green/yellow/gray feedback

Automatically chooses the next word and inputs it for you

Easy to run and no installations necessary

**How to Use**

Open the Wordle website.
 Snap the website to the left of your screen and the terminal with the script to your right.

Run the online_solve.py script.

Press enter when prompted and quickly click back to the wordle website.


**How It Works**

Loads a list of possible 5-letter words accepted by Wordle.

Narrows down possibilities with each guess using the color feedback from the guess.

Chooses high-value next guesses and repeats until the correct word is found or 6 guesses have been made.

License
MIT License
