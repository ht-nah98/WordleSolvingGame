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

# Automatic response based on the comparison between computer's guess and the secret word
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

# Define match_word_vector before it's used
def match_word_vector(word, word_vector):
    assert len(word) == len(word_vector)
    for letter, v_letter in zip(word, word_vector):
        if letter not in v_letter:
            return False
    return True

# Define the match function
def match(word_vector, possible_words):
    return [word for word in possible_words if match_word_vector(word, word_vector)]

# Computer's turn to guess the secret word
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
        
        # Computer's guess
        computer_guess = computer_guess_secret_word(possible_words, word_vector)
        print(f"Computer's guess: {computer_guess}")
        
        # Automatic response based on the comparison
        response = generate_response(secret_word, computer_guess)
        print(f"Automatic response: {response}")
        
        # Update the word vector based on the response
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
        
        # Narrow down the possible words based on the response
        possible_words = match(word_vector, possible_words)
        
        # Check if the computer guessed correctly
        if computer_guess == secret_word:
            print(f"\nComputer guessed the secret word: {secret_word}")
            break

# Provide the secret word for the computer to guess
secret_word = input("Enter the secret word for the computer to guess: ").lower()

# Start the game
play_game(secret_word)
