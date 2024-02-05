import string
from pathlib import Path
from collections import Counter
from itertools import chain
import operator

DICT = "./words_data/words.txt"

ALLOWABLE_CHARACTERS = set(string.ascii_letters)
ALLOWED_ATTEMPTS = 10
WORD_LENGTH = 5

WORDS = {
  word.lower()
  for word in Path(DICT).read_text().splitlines()
  if len(word) == WORD_LENGTH and set(word) < ALLOWABLE_CHARACTERS
}

LETTER_COUNTER = Counter(chain.from_iterable(WORDS))

LETTER_FREQUENCY = {
    character: value / LETTER_COUNTER.total()
    for character, value in LETTER_COUNTER.items()
}

def calculate_word_commonality(word):
    score = 0.0
    for char in word:
        score += LETTER_FREQUENCY[char]
    return score / (WORD_LENGTH - len(set(word)) + 1)

def sort_by_word_commonality(words):
    sort_by = operator.itemgetter(1)
    return sorted(
        [(word, calculate_word_commonality(word)) for word in words],
        key=sort_by,
        reverse=True,
    )

def display_word_table(word_commonalities):
    for (word, freq) in word_commonalities:
        print(f"{word:<10} | {freq:<5.2}")

def generate_response(secret_word, computer_guess):
    response = ""
    for sw, cw in zip(secret_word, computer_guess):
        if sw == cw:
            response += "G"
        elif cw in secret_word:
            response += "Y"
        else:
            response += "?"
    return response

def match_word_vector(word, word_vector):
    assert len(word) == len(word_vector)
    for letter, v_letter in zip(word, word_vector):
        if letter not in v_letter:
            return False
    return True

def match(word_vector, possible_words):
    matching_words = []
    for word in possible_words:
        if match_word_vector(word, word_vector):
            matching_words.append(word)
    return matching_words

def computer_guess_secret_word(possible_words, word_vector):
    sorted_words = sort_by_word_commonality(possible_words)
    for (word, _) in sorted_words:
        if match_word_vector(word, word_vector):
            return word

def play_game(secret_word):
    possible_words = WORDS.copy()
    word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]
    
    for attempt in range(1, ALLOWED_ATTEMPTS + 1):
        print(f"\nAttempt {attempt} with {len(possible_words)} possible words")
        display_word_table(sort_by_word_commonality(possible_words)[:15])

        computer_guess = computer_guess_secret_word(possible_words, word_vector)

        if computer_guess is None:
            print("Computer couldn't guess the secret word.")
            break

        print(f"Computer's guess: {computer_guess}")

        response = generate_response(secret_word, computer_guess)
        print(f"Automatic response: {response}")

        for idx, letter in enumerate(response):
            if letter == "G":
                word_vector[idx] = {computer_guess[idx]}
            elif letter == "Y":
                try:
                    word_vector[idx].remove(computer_guess[idx])
                except KeyError:
                    pass
            elif letter == "?":
                for vector in word_vector:
                    try:
                        vector.remove(computer_guess[idx])
                    except KeyError:
                        pass

        possible_words = match(word_vector, possible_words)

        if computer_guess == secret_word:
            print(f"\nComputer guessed the secret word: {secret_word}")
            break

if __name__ == "__main__":
    secret_word = input("Enter the secret word for the computer to guess: ").lower()

    if len(secret_word) != WORD_LENGTH or not set(secret_word) < ALLOWABLE_CHARACTERS:
        print("Invalid input. Please enter a valid 5-letter word using only allowed characters.")
    else:
        play_game(secret_word)
