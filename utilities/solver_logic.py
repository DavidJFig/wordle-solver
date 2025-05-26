DEBUG = False


def update_word_list(word_list, non_allowed_letters, allowed_letters, correct_letters):
    new_word_list = []

    for word in word_list:
        if DEBUG:
            print(f"\nChecking word: {word}")



        # exclude if allowed letter is in a forbidden position or if allowed letter is missing
        allowed_fail = False
        for letter, bad_positions in allowed_letters.items():
            if letter not in word:
                if DEBUG:
                    print(f"Rejected (allowed letter '{letter}' not in word)")
                allowed_fail = True
                break
            for pos in bad_positions:
                if word[pos] == letter:
                    if DEBUG:
                        print(f"Rejected (letter '{letter}' in disallowed position {pos})")
                    allowed_fail = True
                    break
            if allowed_fail:
                break
        if allowed_fail:
            continue

        # exclude if correct letters not in the correct positions
        correct_fail = False
        for letter, pos in correct_letters.items():
            if word[pos] != letter:
                if DEBUG:
                    print(f"Rejected (expected '{letter}' at position {pos})")
                correct_fail = True
                break
        if correct_fail:
            continue

        # remove letters from non_allowed letters if they are in correct_letters
        for letter in correct_letters.keys():
            if letter in non_allowed_letters:
                if DEBUG:
                    print(f"Removing '{letter}' from non-allowed letters")
                non_allowed_letters.remove(letter)

        # exclude if contains any non-allowed letter
        if any(letter in non_allowed_letters for letter in word):
            if DEBUG:
                print(f"Rejected (non-allowed letter in '{word}')")
            continue

        # if we reach here, the word is valid to consider
        if DEBUG:
            print(f"Accepted word: {word}")
        new_word_list.append(word)

    return new_word_list
