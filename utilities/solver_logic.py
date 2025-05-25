

def update_word_list(word_list, non_allowed_letters, allowed_letters, correct_letters):

    new_word_list = []
    for word in word_list:
        # check if the word contains any non-allowed letters
        if any(letter in non_allowed_letters for letter in word):
            continue


        delete_word = False
        for letter, positions in allowed_letters.items():
            for pos in positions:
                if word[pos] == letter:
                    delete_word = True
                    break
            if delete_word:
                break
        if delete_word:
            continue

        # check if the word does not contain letters in the correct list at the right positions
        if any(word[i] != letter for letter, i in correct_letters.items()):
            continue

        new_word_list.append(word)

    return new_word_list