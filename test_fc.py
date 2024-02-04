import string
from pathlib import Path
from collections import Counter
from itertools import chain
import operator

DICT = "./words_data/words.txt"

ALLOWABLE_CHARACTERS = set(string.ascii_letters)
ALLOWED_ATTEMPTS = 1
WORD_LENGTH = 5

WORDS = {
  word.lower()
  for word in Path(DICT).read_text().splitlines()
  if len(word) == WORD_LENGTH and set(word) < ALLOWABLE_CHARACTERS
}
# print(WORDS)
LETTER_COUNTER = Counter(chain.from_iterable(WORDS))

LETTER_FREQUENCY = {
    character: value / LETTER_COUNTER.total()
    for character, value in LETTER_COUNTER.items()
}

def calculate_word_commonality(word):
    score = 0.0
    for char in word:
        score += LETTER_FREQUENCY[char]
    print(set(word))
    return score / (WORD_LENGTH - len(set(word)) + 1)

def sort_by_word_commonality(words):
    sort_by = operator.itemgetter(1)
    return sorted(
        [(word, calculate_word_commonality(word)) for word in words],
        key=sort_by,
        reverse=True,
    )

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
    print(sorted_words)
    for (word, _) in sorted_words:
        if match_word_vector(word, word_vector):
            return word

# word_vector = [
#     {'a', 'b', 'c', 'd', 'v', 'w', 'x', 'y', 'z'},
#     {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
#     {'a', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
#     {'a', 'b', 'c', 'd', 'e',  'x', 'y', 'z'},
#     {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'v', 'w', 'x', 'y', 'z'}
# ]

# result = match_word_vector(word, word_vector)
# print(result)


secret_word = "apple"
word_vector = [set(string.ascii_lowercase) for _ in range(len(secret_word))]
possible_words = ["table", "apple", "clear", "grape", "zebra", "pluto", "water"]

word = "apple"
result = match_word_vector(word, word_vector)
print(result)

matching_words = match(word_vector, possible_words)
print("matching word",matching_words)

computer_guess = computer_guess_secret_word(possible_words, word_vector)
print("computer guess:",computer_guess)

word = "apple"
word_vector = [
    {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
    {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
    {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
    {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
    {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
]

result = match_word_vector(word, word_vector)
print(result)