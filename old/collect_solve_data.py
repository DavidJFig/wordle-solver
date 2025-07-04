import random
from collections import defaultdict



def update_word_list(word_list, non_allowed_letters, allowed_letters, correct_letters):

    new_word_list = []
    for word in word_list:
        # check if the word contains any non-allowed letters
        if any(letter in non_allowed_letters for letter in word):
            continue


        for letter, positions in allowed_letters.items():
            # check if the word contains the letter in the non allowed positions
            if any(word[i] == letter for i in positions):
                continue

        # check if the word does not contain letters in the correct list at the right positions
        if any(word[i] != letter for letter, i in correct_letters.items()):
            continue

        new_word_list.append(word)

    return new_word_list




if __name__ == "__main__":
    
    # starting word
    #starting_guess = "salet"
     

    num_trials = 1000
    sum_guesses = 0



    for trial in range(num_trials):
        # read word list from file
        with open("shuffled_word_list.txt", "r") as f:
            word_list = f.read().splitlines()
        
        # choose a random word to guess
        word_to_guess = random.choice(word_list).strip()

        starting_guess = random.choice(word_list).strip()
    



        non_allowed_letters = set()          # letters certainly not in the word
        allowed_letters = defaultdict(list)  # letters in the word and the positions they cannot be in
        correct_letters = {}                 # letters in the word and the positions they are certainly in

        for i in range(100):
            #print("Guess #", i + 1)
            if i == 0:
                guess = starting_guess
            else:
                word_list = update_word_list(word_list, non_allowed_letters, allowed_letters, correct_letters)
                guess = random.choice(word_list)
            #print("Guess:", guess)

            if guess == word_to_guess:
                #print("Correct! The word was: ", word_to_guess)
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
        sum_guesses += i + 1
        print("Trial #", trial + 1, "Guesses:", i + 1)
    print("Average guesses:", sum_guesses / num_trials)
        