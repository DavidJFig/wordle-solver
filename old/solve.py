import random
from collections import defaultdict

from solver_logic import update_word_list






if __name__ == "__main__":
    

    max_num_guesses = 50


    # read word list from file
    with open("shuffled_word_list.txt", "r") as f:
        word_list = f.read().splitlines()
    
    # choose a random word to guess
    word_to_guess = random.choice(word_list).strip()
    #word_to_guess = "salet"
    print("Word to guess:", word_to_guess)



    non_allowed_letters = set()          # letters certainly not in the word
    allowed_letters = defaultdict(list)  # letters in the word and the positions they cannot be in
    correct_letters = {}                 # letters in the word and the positions they are certainly in



    # starting word
    starting_guess = "salet"
    #starting_guess = random.choice(word_list).strip()

    for i in range(max_num_guesses):
        print("Guess #", i + 1)
        if i == 0:
            guess = starting_guess
        else:
            word_list = update_word_list(word_list, non_allowed_letters, allowed_letters, correct_letters)
            guess = random.choice(word_list)
        print("Guess:", guess)

        if guess == word_to_guess:
            print("Correct! The word was: ", word_to_guess)
            break



        for index, letter in enumerate(guess):
            if letter in word_to_guess:
                if word_to_guess[index] == letter:
                    correct_letters[letter] = index
                else:
                    if letter not in allowed_letters:
                        allowed_letters[letter].append(index)
            else:
                non_allowed_letters.add(letter)
    