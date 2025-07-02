from collections import Counter
DEBUG = False  # Set to True to enable debug output

def update_word_list(word_list, non_allowed_letters, allowed_letters, correct_letters):
    new_word_list = []

    # Letters that must appear in the word but not at specific positions
    required_letters = set(allowed_letters.keys()) | set(correct_letters.keys())

    for word in word_list:
        if DEBUG:
            print(f"\nChecking word: {word}")

        # Check correct positions
        correct_fail = False
        for letter, pos in correct_letters.items():
            if word[pos] != letter:
                if DEBUG:
                    print(f"Rejected (expected '{letter}' at position {pos})")
                correct_fail = True
                break
        if correct_fail:
            continue

        # Check allowed letters not in forbidden positions
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

        # Count how often each letter appears in the guess
        word_counter = Counter(word)

        # Reject if word contains a non-allowed letter that shouldn't be there at all
        for letter in word_counter:
            if (letter in non_allowed_letters and
                letter not in allowed_letters and
                letter not in correct_letters):
                if DEBUG:
                    print(f"Rejected (non-allowed letter '{letter}' in word)")
                break
        else:
            # Enforce max count logic (e.g., only 1 'u' allowed if 2nd 'u' was gray)
            # Build total allowed count from correct + allowed letters
            max_counts = Counter()
            for letter in allowed_letters:
                max_counts[letter] += 1  # each yellow means at least one
            for letter in correct_letters:
                max_counts[letter] += 1

            over_limit = False
            for letter, count in word_counter.items():
                if letter in max_counts and count > max_counts[letter]:
                    if DEBUG:
                        print(f"Rejected (too many '{letter}' – has {count}, allowed {max_counts[letter]})")
                    over_limit = True
                    break
            if over_limit:
                continue

            if DEBUG:
                print(f"Accepted word: {word}")
            new_word_list.append(word)

    return new_word_list
