import string
import requests
from pathlib import Path
from collections import Counter
from itertools import chain
import operator
import enum

class Tip(enum.Enum):
    ABSENT = 0  # word not in secret word
    PRESENT = 1  # word in secret word but wrong position
    CORRECT = 2  # word in secret word and correct position
# URL to the English words file on GitHub
DICTIONARY_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

ALLOWABLE_CHARACTERS = set(string.ascii_lowercase)
ALLOWED_ATTEMPTS = 6
WORD_LENGTH = 5

# Download the English words file from GitHub
response = requests.get(DICTIONARY_URL)

if response.status_code == 200:
    # Read the content of the response and split lines to get words
    WORDS = {
        word.lower()
        for word in response.text.splitlines()
        if len(word) == WORD_LENGTH and set(word) <= ALLOWABLE_CHARACTERS
    }
else:
    # Handle the case when the download fails
    print(f"Failed to download the English words file from {DICTIONARY_URL}.")
    WORDS = set()  # Set to an empty set or handle it according to your needs

# print(WORDS)

import collections

word = "chess"
score = [Tip.CORRECT, Tip.ABSENT, Tip.ABSENT, Tip.PRESENT, Tip.CORRECT]

# Initialize an empty Counter object
pool = collections.Counter()

# Iterate over each pair of characters in word and score
for char, tip in zip(word, score):
    # Check if the corresponding tip is not Tip.CORRECT (indicating a mismatch)
    if tip != Tip.CORRECT:
        # Increment the count of the mismatched character in the pool
        pool[char] += 1

# The resulting pool will contain counts of characters with non-CORRECT tips
print(pool)